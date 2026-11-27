# Handoff: review

**Role:** feature reviewer. Find defects in this change. You did not write it.
**Lens:** all | blind | edge-case | verification-gap | acceptance | integration

**Repository:** {{repository root}}
**Diff:** `git diff {{baseline}} {{current}} -- . ':(exclude)docs/features'`
**Task file:** {{path; none for blind and edge-case lenses}}
**Other context:** {{intent, plan or design paths for acceptance and integration; else none}}
**Previous findings to confirm fixed:** {{list or none}}

Ignore the task file's "Implementation record" and "Review log" sections.

**You may write:** nothing.

**Return:** findings only, most severe first, each with: severity (`high`, `medium`,
`low`), `path:line`, the concrete failing scenario, evidence, whether this change
introduced it, and a suggested remedy. Then list what you checked and could not check.
An empty list is a valid result; do not invent findings.
