# Contributing

Thanks for helping improve the Agent Marketplace registry. By participating you agree
to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Workflow

1. Fork the repository and create a branch from `main`.
2. Make your change. New skills go in `skills/<name>/SKILL.md`, with any references
   and a license inside the same directory.
3. Run the checks locally (below).
4. Open a pull request against `main`.

`main` is protected: every change lands through a pull request, the `validate` CI
check must pass, review conversations must be resolved, and pull requests are
**squash-merged**. If this is your first contribution, a maintainer has to approve
the workflow run before CI starts.

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

```bash
python3 -m venv .venv && . .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
bash scripts/install-cli.sh "$PWD/.venv/bin"
bash scripts/validate-registry.sh
python3 -m unittest discover -s tests -v
shellcheck scripts/*.sh   # if installed
```

## Reporting bugs and security issues

Use the issue templates for bugs and feature requests. Report security problems
privately as described in [SECURITY.md](SECURITY.md).
