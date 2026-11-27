# Contributing

Thanks for helping improve the Agent Marketplace registry. By participating you agree
to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Workflow

1. Fork the repository and create a branch from `main`.
2. Make your change. New skills go in `skills/<name>/SKILL.md`, with any references
   and a license inside the same directory.
   New subagents go in `agents/<name>.md` with Claude Code subagent front matter
   (`name`, `description`, and optionally `model` and `tools`).
   Follow the [naming rules](#harness-specific-resources) below.
3. Run the checks locally (below).
4. Open a pull request against `main`.

`main` is protected: every change lands through a pull request, the `validate` CI
check must pass, review conversations must be resolved, and pull requests are
**squash-merged**. If this is your first contribution, a maintainer has to approve
the workflow run before CI starts.

## Harness-specific resources

A resource that works with only one harness takes a prefix, both in its file or
directory name and in its `name` field:

| Prefix | Harness |
| --- | --- |
| `cc-` | Claude Code |
| `cx-` | Codex |
| `gc-` | GitHub Copilot |

Resources that work everywhere have no prefix. Add every new resource to
[.github/registry-check.yaml](.github/registry-check.yaml) and to the configuration
example in the README, putting prefixed ones in their harness's group. Agent
Marketplace has no GitHub Copilot target, so `gc-` resources cannot be checked yet.

## Pull request titles

The PR title becomes the squash commit message, and release-please builds the
changelog and version from it. Use a [Conventional Commit](https://www.conventionalcommits.org/)
title; CI rejects anything else:

```
<type>(<optional scope>)!: <description>
```

Allowed types: `feat`, `fix`, `docs`, `chore`, `ci`, `test`, `refactor`, `perf`,
`build`, `style`, `revert`. Examples: `feat: add terraform-modules skill`,
`fix(git): correct rebase instructions`.

## Running checks locally

Validation is done by the Agent Marketplace CLI. Install the pinned version, then
sync your checkout into a throwaway project. The temporary `HOME` keeps your own
configuration and harness directories out of the run.

```bash
bash scripts/install-cli.sh "$HOME/.local/bin"
work=$(mktemp -d)
mkdir -p "$work/home" "$work/consumer/.agents"
cp -R . "$work/consumer/registry"
cp .github/registry-check.yaml "$work/consumer/.agents/config.yaml"
git init --quiet "$work/consumer"
(cd "$work/consumer" && HOME="$work/home" agent-marketplace sync --strict --verbose)
(cd "$work/consumer" && HOME="$work/home" agent-marketplace list)
shellcheck scripts/*.sh   # if installed
```

The sync must succeed and report `Malformed 0  Errors 0`, and the list must show no
resource as `available`.

## Reporting bugs and security issues

Use the issue templates for bugs and feature requests. Report security problems
privately as described in [SECURITY.md](SECURITY.md).
