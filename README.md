# Agent Marketplace Registry

[![CI](https://github.com/rafaelherik/agent-marketplace/actions/workflows/ci.yml/badge.svg)](https://github.com/rafaelherik/agent-marketplace/actions/workflows/ci.yml)
[![Release](https://github.com/rafaelherik/agent-marketplace/actions/workflows/release.yml/badge.svg)](https://github.com/rafaelherik/agent-marketplace/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A versioned Git registry of reusable agent skills for
[Agent Marketplace](https://agent-marketplace.io/). Install selected skills into the
native folders of Claude Code, Factory Droid, Cursor, Windsurf, Gemini CLI, Devin CLI,
Codex, or OpenCode.

## Available skills

| Skill | Purpose | Runtime requirements |
| --- | --- | --- |
| [context-hub](skills/context-hub/SKILL.md) | Verify third-party API usage against documentation for the project's resolved dependency versions. | Context Hub MCP or `chub`, with an official HTTPS documentation fallback through the host's fetch/browser tool. |
| [terraform-modules](docs/skills/terraform-modules.md) | Create, review, refactor, document, and test reusable Terraform modules using provider-neutral best practices. | Terraform CLI for checks; official documentation access. Native tests require 1.6+, mocks 1.7+; uses configured TFLint and terraform-docs when available. |

The registry uses `skills/<name>/SKILL.md`. References and the license inside each
skill directory ship with the skill. Agent Marketplace discovers this layout directly;
there is no registry manifest to generate or package to build.

## Install

### 1. Set up Agent Marketplace

You need Git, macOS or Linux, and the Agent Marketplace CLI on your `PATH`.
Validation and the commands in this README target **v5.1.1**. The CLI version is
independent of this registry's release version.

The upstream installer installs the current release:

```bash
curl -fsSL https://agent-marketplace.io/install.sh | bash
agent-marketplace --version
```

To install the exact version used by this registry, clone this repository and run:

```bash
bash scripts/install-cli.sh "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
```

The helper downloads the version in `.github/agent-marketplace-version` and verifies
the binary against the release's `SHA256SUMS`.

On a fresh installation, choose your target harnesses (replace this list as needed):

```bash
agent-marketplace init --harnesses claude,codex,opencode
```

For an existing installation, edit `harnesses` in `~/.agents/config.yaml`, or use the
TUI's harness selector. See [upstream setup](https://agent-marketplace.io/docs/quick-start).

### 2. Install a released skill

Run this inside the consuming project's Git repository. **The example requires the
first `v1.0.0` release to have been published**; before then, use the local development
instructions below. Choose an existing tag from [Releases](https://github.com/rafaelherik/agent-marketplace/releases).

```bash
agent-marketplace install context-hub \
  --from https://github.com/rafaelherik/agent-marketplace \
  --ref v1.0.0 \
  --scope repo
```

Commit the generated `.agents/config.yaml` and `.agents/lock.yaml`. Teammates run
`agent-marketplace sync` to install the locked revision. Keep generated harness
skill folders out of version control; commit the source selection and lock instead.

For skills available to you across projects, use `--scope user` instead. Its config
and lock live at `~/.agents/config.yaml` and `~/.agents/lock.yaml`. `--scope local`
selects resources privately for one checkout, using `.agents/config.local.yaml`
and `.agents/lock.local.yaml`.

Equivalent repository configuration:

```yaml
apiVersion: agent-marketplace/v4
harnesses: [claude, codex, opencode]
sources:
  rafaelherik:
    git: https://github.com/rafaelherik/agent-marketplace
    ref: v1.0.0
    source_harness: claude
resources:
  rafaelherik:
    include:
      - skill/context-hub
```

`source_harness: claude` describes the registry's input layout; it does not limit
the destination harnesses. After writing this configuration, run `agent-marketplace sync`.

### 3. Configure documentation access

Installing `context-hub` installs instructions and reference files. Configure its
documentation access separately using either:

- **Context Hub CLI:** install [Context Hub](https://github.com/andrewyng/context-hub)
  with `npm install -g @aisuite/chub@0.1.4` (Node.js 18+), then verify `chub help`.
- **Context Hub MCP:** the same package provides the `chub-mcp` executable. Add it
  as a stdio MCP server in your harness. For example, a Claude-style configuration is:

  ```json
  {
    "mcpServers": {
      "context-hub": {
        "command": "chub-mcp",
        "args": []
      }
    }
  }
  ```

  Other harnesses use their native MCP configuration format. The host may prefix
  `chub_search`, `chub_get`, and `chub_list` differently.
- **Official documentation fallback:** enable a fetch/browser tool capable of
  reading public HTTPS documentation. The skill uses this when Context Hub is
  unavailable or does not cover the required version. With no retrieval tool, it
  asks for documentation and labels claims unverified.

## Update and roll back

### Patch updates

Preview and apply updates for this registry only:

```bash
agent-marketplace update --scope repo \
  --registry https://github.com/rafaelherik/agent-marketplace \
  --bump --dry-run

agent-marketplace update --scope repo \
  --registry https://github.com/rafaelherik/agent-marketplace \
  --bump

git diff -- .agents/config.yaml .agents/lock.yaml
agent-marketplace sync --strict --check
```

Commit both files after reviewing the changelog and testing the updated skill.
For user-wide installs, explicitly use `--scope user`; back up the user config and
lock before applying changes. `update` otherwise defaults to multiple scopes.

**Tag behavior matters:**

- `sync` reproduces the lock; plain `update` respects the configured tag.
- `update --bump` finds the greatest trailing number with the same prefix:
  `v1.0.0` can move to `v1.0.7`, but not `v1.1.0` or `v2.0.0`.
- For minor/major releases, edit the source's `ref` in the owning config, run
  `agent-marketplace sync`, then review and commit config and lock together.
- Refs in included configuration fragments must be edited in those fragments.
- Full tags are permanent. Directory sources read live files and are never locked
  or advanced by `--bump`.

### Rollback

For a committed upgrade, revert its commit and sync:

```bash
git revert <upgrade-commit>
agent-marketplace sync
agent-marketplace sync --strict --check
```

For an uncommitted upgrade, restore **both** config and lock to the desired version
(save unrelated edits first), then sync. User-wide rollback likewise restores both
backed-up files. A plain sync can fetch an old snapshot if it is no longer cached.

## Develop and validate

Clone the registry, install the pinned CLI, and prepare Python 3.9+:

```bash
git clone https://github.com/rafaelherik/agent-marketplace.git
cd agent-marketplace
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
bash scripts/install-cli.sh "$PWD/.venv/bin"
bash scripts/validate-registry.sh
python3 -m unittest discover -s tests -v
```

Validation checks the expected inventory, skill metadata, bundled reference links,
license, and release version files. It then tests actual discovery and compilation
for all eight harnesses, verifies support files, and checks for drift in both symlink
and regular-file modes against a snapshot of Git-visible files (including new,
unignored files). Empty placeholder directories are not published by Git and are
excluded from that snapshot. The tests also exercise tagged installs, dry-run updates,
patch-only bumps, explicit minor upgrades, and rollback using a temporary Git registry.

Temporary consumers, home directories, and state are cleaned up automatically.
Run validation on a machine without `/etc/agent-marketplace/config.yaml`; the CLI's
fixed organization configuration cannot be isolated with `HOME`.

To try changes in your own consuming project, add a local source to its configuration:

```yaml
apiVersion: agent-marketplace/v4
harnesses: [claude, codex, opencode]
sources:
  development:
    directory: /absolute/path/to/agent-marketplace
    source_harness: claude
resources:
  development:
    include: [skill/context-hub]
```

Then run `agent-marketplace sync` after editing skills. Select either the development
source or the released source for the same skill to avoid a name collision.

### Add or change a skill

1. Create `skills/<lowercase-hyphenated-name>/SKILL.md` with `name`, a useful
   `description`, and `license: MIT` in YAML front matter.
2. Copy the root `LICENSE` into the skill folder and keep references inside that
   folder, linked with relative Markdown links.
3. Document runtime prerequisites and use available host tool names rather than
   hard-coded MCP prefixes.
4. Add the name to `.github/expected-skills.txt` and the catalog above.
5. Run validation and open a PR with a Conventional Commit title.

## Releases and GitHub setup

This registry versions all skills together using semantic versions and
[release-please](https://github.com/googleapis/release-please-action).

| Squash commit | Version effect |
| --- | --- |
| `fix: correct dependency lookup` | Patch |
| `feat: add a skill` | Minor |
| `feat!: rename or remove a skill` | Major |
| `docs: clarify repository setup` / `ci: improve validation` | No release on their own |

Use `fix:` for corrections to shipped skill instructions, even though those files
are Markdown. Mark changes consumers must adapt to with `!` or a `BREAKING CHANGE:`
footer. Squash-merge PRs using their validated titles.

On pushes to `main`, the Release workflow runs CI, then release-please maintains a
release PR updating `version.txt`, `CHANGELOG.md`, and `.release-please-manifest.json`.
After that PR is merged and validation passes, release-please creates the matching
`vX.Y.Z` tag and GitHub Release. Consumers install directly from Git tags.

The initial empty manifest means there is no previous release. `version.txt` starts
at `0.0.0`; the first release PR proposes `1.0.0`. Merge or push a `feat:`/`fix:` commit
to start the first release. Subsequent versions follow Conventional Commits. Do not
manually advance version files or move existing release tags.

### One-time maintainer setup

1. Create or grant access to `rafaelherik/agent-marketplace` on GitHub, use `main` as
   its default branch, and push the initial files. If this checkout has no remote:
   `git remote add origin https://github.com/rafaelherik/agent-marketplace.git`.
2. Enable GitHub Actions and, when using `GITHUB_TOKEN`, **Allow GitHub Actions to
   create and approve pull requests** in Settings → Actions → General.
3. For automatic CI on release PRs, add a fine-grained PAT as the Actions secret
   `RELEASE_PLEASE_TOKEN`, scoped to this repository with **Contents**, **Pull requests**,
   and **Issues** read/write. Keep the token valid and rotate it before expiry.
   A GitHub App installation token can be supplied instead by adapting token creation
   in the release job.
4. Without that secret, the workflow uses `GITHUB_TOKEN`. GitHub currently requires
   approval to run CI on PRs opened/updated by this token; approve those runs before
   merging the release PR. Token-created tag/release events do not start downstream
   workflows. This setup publishes directly in the Release workflow.
5. Enable squash merging, use PR titles for squash messages, and require the CI
   `validate` check on `main` (select the check shown after its first run).

CI uses read-only repository permissions. Only the release job has write permissions.
The Release workflow can be rerun from Actions after fixing credentials or settings.

## References

- [Registry layout](https://agent-marketplace.io/docs/reference/registry-layout)
- [Validate a registry in CI](https://agent-marketplace.io/docs/how-to/author/validate-a-registry-in-ci)
- [Version and release a registry](https://agent-marketplace.io/docs/how-to/author/version-and-release-a-registry)
- [Configuration reference](https://agent-marketplace.io/docs/reference/configuration)
- [GitHub workflow triggering and token behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)

Some upstream guides describe older CLI versions. In particular, v5.1.1 provides
`update --dry-run`; use `agent-marketplace <command> --help` for the pinned version.

## License

[MIT](LICENSE). Each distributed skill includes a copy of the license.
