# Agent Marketplace Registry

[![CI](https://github.com/rafaelherik/agent-marketplace/actions/workflows/ci.yml/badge.svg)](https://github.com/rafaelherik/agent-marketplace/actions/workflows/ci.yml)
[![Release](https://github.com/rafaelherik/agent-marketplace/actions/workflows/release.yml/badge.svg)](https://github.com/rafaelherik/agent-marketplace/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A versioned collection of reusable agent skills and subagents for
[Agent Marketplace](https://agent-marketplace.io/), supporting Claude Code,
Factory Droid, Cursor, Windsurf, Gemini CLI, Devin CLI, Codex, and OpenCode.

## Available skills

| Skill | Purpose |
| --- | --- |
| [context-hub](skills/context-hub/SKILL.md) | Verify third-party API usage against documentation for the project's dependency versions. |
| [feature-implementation](docs/skills/feature-implementation.md) | Clarify, design, plan, implement, review and approve a feature with specialist agents. |
| [terraform-modules](docs/skills/terraform-modules.md) | Create, review, refactor, document, and test reusable Terraform modules. |

Skills live in `skills/<name>/SKILL.md`, with bundled references and licenses.
The registry versions all skills and subagents together using semantic releases.

## Available agents

| Agent | Model | Purpose |
| --- | --- | --- |
| [cc-explorer](agents/cc-explorer.md) | Haiku | Fast, read-only codebase exploration in Claude Code. |
| [cx-explorer](agents/cx-explorer.md) | GPT-6 Luna | Fast, read-only codebase exploration in Codex. |
| [feature-analyst](agents/feature-analyst.md) | Harness default | Clarify a request into a testable intent. |
| [backend-architect](agents/backend-architect.md) | Harness default | Design and conformance review of backend changes. |
| [frontend-architect](agents/frontend-architect.md) | Harness default | Design and conformance review of frontend changes. |
| [platform-architect](agents/platform-architect.md) | Harness default | Design and conformance review of infrastructure and platform changes. |
| [feature-planner](agents/feature-planner.md) | Harness default | Split a design into ordered task files. |
| [feature-developer](agents/feature-developer.md) | Harness default | Implement one task with tests. |
| [feature-reviewer](agents/feature-reviewer.md) | Harness default | Adversarial review of a task diff. |
| [feature-approver](agents/feature-approver.md) | Harness default | Verify criteria and give an approval verdict. |

Subagents live in `agents/<name>.md`. A `cc-`, `cx-` or `gc-` prefix marks a
resource specific to Claude Code, Codex or GitHub Copilot.

Select each prefixed agent for its own harness only. Selecting `cc-explorer` for
Codex or Cursor makes the sync fail, because they cannot express its tool restriction.
In `.agents/config.yaml`, name what you want and give prefixed agents their own source
groups. Do not combine these groups with `all: true`, which can silently drop agents.

```yaml
sources:
  shared: {git: "https://github.com/rafaelherik/agent-marketplace", ref: <tag>}
  claude-code: {git: "https://github.com/rafaelherik/agent-marketplace", ref: <tag>}
  codex: {git: "https://github.com/rafaelherik/agent-marketplace", ref: <tag>}
resources:
  shared:
    include:
      - skill/context-hub
      - skill/feature-implementation
      - skill/terraform-modules
      - subagent/feature-analyst
      - subagent/backend-architect
      - subagent/frontend-architect
      - subagent/platform-architect
      - subagent/feature-planner
      - subagent/feature-developer
      - subagent/feature-reviewer
      - subagent/feature-approver
  claude-code:
    include: [subagent/cc-explorer]
    harnesses: [claude]
  codex:
    include: [subagent/cx-explorer]
    harnesses: [codex]
```

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
