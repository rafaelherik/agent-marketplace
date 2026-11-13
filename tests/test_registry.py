"""Regression checks for validation failures and the documented consumer lifecycle."""

from pathlib import Path
import shutil
import tempfile
import unittest

import yaml

from scripts.validate_registry import ROOT, cli_path, run, sandbox, validate_metadata, write_config


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="registry-metadata-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "skills", self.root / "skills")
        (self.root / ".github").mkdir()
        shutil.copy(ROOT / ".github/expected-skills.txt", self.root / ".github")
        shutil.copy(ROOT / "LICENSE", self.root)
        self.skill = self.root / "skills/context-hub/SKILL.md"

    def test_missing_skill_cannot_pass_as_empty_catalog(self):
        self.skill.unlink()
        with self.assertRaisesRegex(ValueError, "do not match"):
            validate_metadata(self.root)

    def test_invalid_yaml_is_rejected(self):
        self.skill.write_text("---\nname: [\n---\nBody\n")
        with self.assertRaises(yaml.YAMLError):
            validate_metadata(self.root)

    def test_mismatched_name_is_rejected(self):
        self.skill.write_text(self.skill.read_text().replace("name: context-hub", "name: another-skill"))
        with self.assertRaisesRegex(ValueError, "mismatched name"):
            validate_metadata(self.root)

    def test_missing_bundled_reference_is_rejected(self):
        (self.skill.parent / "references/version-resolution.md").unlink()
        with self.assertRaisesRegex(ValueError, "non-bundled reference"):
            validate_metadata(self.root)


class TaggedUpdateTests(unittest.TestCase):
    def test_install_preview_patch_minor_upgrade_and_rollback(self):
        binary = cli_path()
        with sandbox() as (work, env):
            env.update(GIT_AUTHOR_NAME="Registry Test", GIT_AUTHOR_EMAIL="test@example.invalid",
                       GIT_COMMITTER_NAME="Registry Test", GIT_COMMITTER_EMAIL="test@example.invalid")
            registry = work / "registry"
            shutil.copytree(ROOT / "skills", registry / "skills")
            run(["git", "init", "--quiet", str(registry)], work, env)
            skill = registry / "skills/context-hub/SKILL.md"
            original = skill.read_text()
            for tag, marker in (("v1.0.0", "Original release"), ("v1.0.1", "Patch release"),
                                ("v1.1.0", "Minor release")):
                skill.write_text(original + f"\n{marker}\n")
                run(["git", "add", "."], registry, env)
                run(["git", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", f"feat: {marker}"], registry, env)
                run(["git", "tag", tag], registry, env)

            consumer = work / "consumer"
            consumer.mkdir()
            run(["git", "init", "--quiet", str(consumer)], work, env)
            config = consumer / ".agents/config.yaml"
            # install --from file:// becomes a live directory source in v5.1.1.
            # An explicit Git source exercises real tag acquisition and lockfiles.
            write_config(config, {
                "apiVersion": "agent-marketplace/v4", "harnesses": ["claude"],
                "sources": {"registry": {"git": registry.as_uri(), "ref": "v1.0.0"}},
                "resources": {"registry": {"include": ["skill/context-hub"]}},
            })
            run([binary, "sync", "--strict"], consumer, env)
            lock = consumer / ".agents/lock.yaml"
            installed = consumer / ".claude/skills/context-hub/SKILL.md"
            original_config, original_lock = config.read_bytes(), lock.read_bytes()
            self.assertIn("Original release", installed.read_text())
            self.assertTrue((installed.parent / "references/version-resolution.md").is_file())
            target = ["--scope", "repo", "--registry", registry.as_uri()]

            run([binary, "update", *target], consumer, env)
            self.assertIn("Original release", installed.read_text(), "Plain update must respect the pinned tag")
            before = (config.read_bytes(), lock.read_bytes(), installed.read_bytes())
            run([binary, "update", *target, "--bump", "--dry-run"], consumer, env)
            self.assertEqual(before, (config.read_bytes(), lock.read_bytes(), installed.read_bytes()))
            run([binary, "update", *target, "--bump"], consumer, env)
            self.assertIn("Patch release", installed.read_text())
            data = yaml.safe_load(config.read_text())
            source = next(iter(data["sources"].values()))
            self.assertEqual(source["ref"], "v1.0.1", "--bump must not cross to v1.1.0")

            source["ref"] = "v1.1.0"
            write_config(config, data)
            run([binary, "sync", "--strict"], consumer, env)
            self.assertIn("Minor release", installed.read_text())
            config.write_bytes(original_config)
            lock.write_bytes(original_lock)
            run([binary, "sync", "--locked", "--strict"], consumer, env)
            self.assertIn("Original release", installed.read_text())
            run([binary, "sync", "--strict", "--check"], consumer, env)


if __name__ == "__main__":
    unittest.main()
