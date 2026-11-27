# Feature implementation

[Back to registry](../../README.md#available-skills)

The `feature-implementation` skill takes a feature from request to verified change. An
orchestrator clarifies intent with you, has domain architects design it, plans small
tasks, and implements, reviews and approves each one. Each phase runs in a specialist
subagent with a clean context.

Inspired by the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD): phase
specialists, task files as the handoff contract, size and risk based tracks, layered
adversarial review with triage, and human approval. It is an independent, smaller design,
not a port, and needs no BMAD installation.

## Install

Select the skill and all eight agents:

```yaml
resources:
  shared:
    include:
      - skill/feature-implementation
      - subagent/feature-analyst
      - subagent/backend-architect
      - subagent/frontend-architect
      - subagent/platform-architect
      - subagent/feature-planner
      - subagent/feature-developer
      - subagent/feature-reviewer
      - subagent/feature-approver
```

The agents set no model or tool restriction, so they work across harnesses and use the
harness's defaults. "Read-only" for the reviewer and approver is therefore an instruction,
not an enforced permission.

## Example requests

- "Use feature-implementation to add CSV export to the reports page."
- "Implement team invitations: API, UI and the email queue infrastructure."
- "Resume the feature in docs/features/team-invitations."

## What you decide

| Gate | You approve |
| --- | --- |
| G1 | Goal, scope, acceptance criteria and track |
| G2 | Design and plan; approval mode and commit policy |
| G3 | Each task (unless you delegate it) |
| G4 | The finished feature and any rollout steps |

## Files it creates

`docs/features/<slug>/` holds the intent, designs, plan, task files and deferred items.
Keep or ignore them as your repository prefers.

See the [skill](../../skills/feature-implementation/SKILL.md), the
[workflow reference](../../skills/feature-implementation/references/workflow.md) and the
[handoff templates](../../skills/feature-implementation/references/handoffs/).
