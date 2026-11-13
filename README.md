# Agent Marketplace Registry

[![CI](https://github.com/rafaelherik/agent-marketplace/actions/workflows/ci.yml/badge.svg)](https://github.com/rafaelherik/agent-marketplace/actions/workflows/ci.yml)
[![Release](https://github.com/rafaelherik/agent-marketplace/actions/workflows/release.yml/badge.svg)](https://github.com/rafaelherik/agent-marketplace/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A versioned collection of reusable agent skills for
[Agent Marketplace](https://agent-marketplace.io/), supporting Claude Code,
Factory Droid, Cursor, Windsurf, Gemini CLI, Devin CLI, Codex, and OpenCode.

## Available skills

| Skill | Purpose |
| --- | --- |
| [context-hub](skills/context-hub/SKILL.md) | Verify third-party API usage against documentation for the project's dependency versions. |
| [terraform-modules](docs/skills/terraform-modules.md) | Create, review, refactor, document, and test reusable Terraform modules. |

Skills live in `skills/<name>/SKILL.md`, with bundled references and licenses.
The registry versions all skills together using semantic releases.

## Getting started

Visit [Agent Marketplace](https://agent-marketplace.io/) for installation and
usage instructions. Use this repository as your skill registry:
[rafaelherik/agent-marketplace](https://github.com/rafaelherik/agent-marketplace).

- [Quick start](https://agent-marketplace.io/docs/quick-start)
- [Configuration reference](https://agent-marketplace.io/docs/reference/configuration)
- [Registry layout](https://agent-marketplace.io/docs/reference/registry-layout)

## Project links

- [Contributing](CONTRIBUTING.md)
- [Releases](https://github.com/rafaelherik/agent-marketplace/releases) and [changelog](CHANGELOG.md)
- [Issues](https://github.com/rafaelherik/agent-marketplace/issues)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)

## License

[MIT](LICENSE). Each distributed skill includes a copy of the license.
