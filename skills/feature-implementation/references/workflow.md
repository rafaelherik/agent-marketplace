# Workflow reference

## Feature folder

```text
docs/features/<slug>/
  intent.md            from artifacts/intent.md
  design-<domain>.md   from artifacts/design.md (backend, frontend, platform)
  plan.md              from artifacts/plan.md
  tasks/NN-<name>.md   from artifacts/task.md
  deferred.md          out-of-scope findings, one bullet each with its source
```

Templates: [intent](artifacts/intent.md), [design](artifacts/design.md),
[plan](artifacts/plan.md), [task](artifacts/task.md).

## Ownership

| File or section | Writer |
| --- | --- |
| `intent.md` | analyst (orchestrator records the user's confirmation) |
| `design-<domain>.md` | that domain's architect |
| `plan.md` task list; task contract sections | planner (orchestrator on the quick track) |
| Task "Implementation record" | developer |
| Task "Review log" and "Approval"; every status; `deferred.md` | orchestrator |
| Product code and tests | developer |

Reviewer and approver write nothing; they return reports that you record. A task's
contract sections are frozen once it starts. Changing them means returning to planning.

## Statuses

`ready` -> `in-progress` -> `in-review` -> `awaiting-approval` -> `done`

`changes-requested` returns to `in-progress`. `blocked` records its reason and what would
unblock it. Keep the status in the task file and the `plan.md` table identical.

## Task loop

### Snapshot

A snapshot is a git tree of the working directory, including untracked files. It does not
touch the real index, the branch or the stash:

```bash
idx=$(mktemp)
cp "$(git rev-parse --git-path index)" "$idx" 2>/dev/null || rm -f "$idx"
GIT_INDEX_FILE="$idx" git add -A && GIT_INDEX_FILE="$idx" git write-tree
rm -f "$idx"
```

Run it from the repository root. Record the result as the task's `baseline` before the
developer starts, and take a new one before each review. The task diff is:

```bash
git diff <baseline> <current> -- . ':(exclude)docs/features'
```

Keep the baseline across fix rounds, so every review sees the complete task. Changes that
existed before the baseline stay out of the diff. The feature diff uses the first task's
baseline.

### Review depth

| Track | Reviewers |
| --- | --- |
| Quick, standard | One `feature-reviewer` with lens `all` |
| High-risk | Four in parallel: `blind`, `edge-case`, `verification-gap`, `acceptance`; plus the domain architect with a conformance review |

| Lens | Question | Gets the task file |
| --- | --- | --- |
| `blind` | What is wrong or missing in this diff on its own? | No |
| `edge-case` | Which inputs, states, failures and races are unhandled? | No |
| `verification-gap` | Which behavior would break without any test failing? | Yes |
| `acceptance` | Does the diff do what the task and intent ask, and nothing else? | Yes |
| `integration` | Do the tasks fit together: contracts, wiring, migration order, rollout? | Plan and designs |

## Triage

Check every finding at its cited location before acting; reviewers can be wrong. Merge
duplicates, then put each in one bucket:

| Bucket | When | Action |
| --- | --- | --- |
| `fix` | Real, introduced by this change, remedy is clear | Send to the developer |
| `decision` | Needs a product or design choice | Ask the user |
| `replan` | The intent, design or task is wrong | Return to that phase |
| `defer` | Real but pre-existing or out of scope | Add to `deferred.md` |
| `dismiss` | False, or too unlikely and minor to matter | Record the reason |

Defects introduced by the change that are `high` or `medium` severity are never deferred.
Record findings, buckets and outcomes in the task's "Review log".

## Resume

Trust the files and the working tree over memory. Continue at the earliest unpassed gate.
For an unfinished task:

| Status | Next step |
| --- | --- |
| `ready` | Take a baseline and implement |
| `in-progress`, `changes-requested` | Give the developer the existing diff and open findings |
| `in-review` | Review again |
| `awaiting-approval` | Check the tree still matches the approved evidence, then ask the user |
| `blocked` | Ask the user about the recorded blocker |

If a recorded baseline no longer resolves (`git cat-file -e <tree>` fails), ask the user
which commit to diff against.
