"""Validate authored skills and their real Agent Marketplace installations."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager

import yaml

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    name: f".{name}/skills"
    for name in ("claude", "factory", "cursor", "windsurf", "gemini", "devin", "opencode")
}
TARGETS["codex"] = ".agents/skills"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(args, cwd, env):
    result = subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=False)
    print(result.stdout, end="", flush=True)
    result.check_returncode()
    return result.stdout


def write_config(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


@contextmanager
def sandbox():
    # The CLI always reads this fixed path; HOME cannot isolate organization policy.
    require(not Path("/etc/agent-marketplace/config.yaml").exists(),
            "Run validation on a clean runner without organization configuration.")
    with tempfile.TemporaryDirectory(prefix="registry-check-") as directory:
        work = Path(directory).resolve()
        home = work / "home"
        home.mkdir()
        env = {key: value for key, value in os.environ.items()
               if not key.startswith(("GIT_", "AGENT_MARKETPLACE_", "XDG_", "OPENCODE_"))
               and key not in ("CLAUDE_CONFIG_DIR", "CODEX_HOME")}
        env.update(HOME=str(home), XDG_STATE_HOME=str(home / "state"),
                   XDG_CONFIG_HOME=str(home / ".config"), NO_COLOR="1", CI="true",
                   GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                   AGENT_MARKETPLACE_TELEMETRY_LEVEL="off",
                   AGENT_MARKETPLACE_LOG_ENABLED="false")
        write_config(home / ".agents/config.yaml",
                     {"apiVersion": "agent-marketplace/v4", "harnesses": list(TARGETS)})
        yield work, env


def validate_metadata(root):
    expected = (root / ".github/expected-skills.txt").read_text().splitlines()
    require(expected and len(expected) == len(set(expected)), "Expected skill list is empty or duplicated")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    require(set(root.glob("skills/**/SKILL.md")) == set(skills), "Skills must be directly under skills/<name>/")
    require({path.parent.name for path in skills} == set(expected),
            "Skill folders do not match .github/expected-skills.txt")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", text, re.DOTALL)
        require(match, f"{path}: missing front matter or body")
        metadata = yaml.safe_load(match[1])
        require(isinstance(metadata, dict), f"{path}: front matter must be a mapping")
        name = metadata.get("name")
        require(isinstance(name, str) and re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name)
                and len(name) <= 64 and name == path.parent.name, f"{path}: invalid or mismatched name")
        description = metadata.get("description")
        require(isinstance(description, str) and 0 < len(description.strip()) <= 1024,
                f"{path}: description must contain 1–1024 characters")
        require(metadata.get("license") == "MIT", f"{path}: declare license: MIT")
        require((path.parent / "LICENSE").read_bytes() == (root / "LICENSE").read_bytes(),
                f"{path}: bundle the repository MIT license")
        for markdown in path.parent.rglob("*.md"):
            for link in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", markdown.read_text()):
                if ":" not in link and not link.startswith("#"):
                    target = (markdown.parent / link.split("#")[0]).resolve()
                    require(target.is_file() and path.parent.resolve() in target.parents,
                            f"{markdown}: missing or non-bundled reference {link}")
    return expected


def validate_release_files(root):
    config = json.loads((root / "release-please-config.json").read_text())
    package = config["packages"]["."]
    require(package["release-type"] == "simple" and not package["include-component-in-tag"]
            and package["include-v-in-tag"], "Registry must release as vX.Y.Z")
    version = (root / "version.txt").read_text().strip()
    require(re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version),
            "version.txt must contain a stable semantic version")
    manifest = json.loads((root / ".release-please-manifest.json").read_text())
    if not manifest:
        require(version == "0.0.0" and package["initial-version"] == "1.0.0",
                "An empty manifest is only valid before the first release")
    else:
        require(manifest == {".": version}, "Release manifest and version.txt disagree")
        changelog = (root / "CHANGELOG.md").read_text()
        require(re.search(r"^## (?:\[)?" + re.escape(version) + r"(?:\]|\s|$)", changelog, re.MULTILINE),
                "Current version is missing from CHANGELOG.md")


def cli_path():
    binary = shutil.which("agent-marketplace")
    require(binary, "Install Agent Marketplace with bash scripts/install-cli.sh first")
    expected = (ROOT / ".github/agent-marketplace-version").read_text().strip()
    actual = subprocess.check_output([binary, "--version"], text=True).strip()
    require(actual == expected, f"Expected CLI {expected}, found {actual}")
    return binary


def verify_outputs(consumer, registry, names):
    for target, output in TARGETS.items():
        for name in names:
            source = registry / "skills" / name
            installed = consumer / output / name
            require((installed / "SKILL.md").is_file(), f"{target}: missing skill {name}")
            for support in source.rglob("*"):
                if support.is_file() and support.name != "SKILL.md":
                    destination = installed / support.relative_to(source)
                    require(destination.is_file() and destination.read_bytes() == support.read_bytes(),
                            f"{target}: missing or changed support file {support}")


def snapshot_registry(destination, env):
    # Match a Git checkout: ignore local-only files and empty placeholder folders.
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, env=env,
    )
    for name in set(output.decode().split("\0")) - {""}:
        source = ROOT / name
        if source.is_file():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def validate_installation(binary, names):
    with sandbox() as (work, env):
        registry = work / "registry"
        snapshot_registry(registry, env)
        consumer = work / "consumer"
        config_path = consumer / ".agents/config.yaml"
        config = {
            "apiVersion": "agent-marketplace/v4", "harnesses": list(TARGETS),
            "sources": {"checkout": {"directory": str(registry), "source_harness": "claude"}},
            "resources": {"checkout": {"all": True, "required": True}},
        }
        write_config(config_path, config)
        run(["git", "init", "--quiet", str(consumer)], work, env)
        listing = run([binary, "list", "--kind", "skill"], consumer, env)
        discovered = re.findall(r"^\S+\s+skill\s+(\S+)", listing, re.MULTILINE)
        require(sorted(discovered) == sorted(names), "CLI discovery does not match expected skills")
        for mode in ("symlink", "file"):
            config["materialization"] = {"mode": mode}
            write_config(config_path, config)
            output = run([binary, "sync", "--strict", "--verbose"], consumer, env)
            require(re.search(r"Malformed\s+0\s+Errors\s+0\b", output), "Malformed resources or compilation errors")
            run([binary, "sync", "--strict", "--check"], consumer, env)
            verify_outputs(consumer, registry, names)
        require(not (consumer / ".agents/lock.yaml").exists(), "Directory sources must not create an acquisition lock")


if __name__ == "__main__":
    try:
        names = validate_metadata(ROOT)
        validate_release_files(ROOT)
        validate_installation(cli_path(), names)
        print(f"Validated {len(names)} skill(s) across {len(TARGETS)} harnesses in both materialization modes.")
    except (ValueError, OSError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Validation failed: {error}") from error
