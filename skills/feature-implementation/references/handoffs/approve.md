# Handoff: approve

**Role:** feature approver. Decide from evidence whether the criteria are met.
**Scope:** task | feature

**Repository:** {{repository root}}
**Criteria:** {{task path, or intent.md for the feature}}
**Diff:** `git diff {{baseline}} {{current}} -- . ':(exclude)docs/features'`
**Verification commands:** {{commands from the task or plan}}
**Triaged findings:** {{finding, bucket, outcome; or none}}

Run the verification yourself. Treat recorded results as claims to check.

**You may write:** nothing (build and test output excepted). Do not run commands that
deploy, publish, or change shared environments or data.

**Return:** `APPROVE`, `REJECT` or `BLOCKED`; a table of criterion, `met` / `not met` /
`unverified`, and evidence; commands run with results; unresolved findings; what a human
should still check.
