# Handoff: design

**Role:** {{backend | frontend | platform}} architect.
**Mode:** design | revise | conformance review

**Repository:** {{repository root}}
**Read:** `{{feature folder}}/intent.md`, repository instructions, {{other design files}}
**Design template:** {{contents of artifacts/design.md}}
**Revision requests or contract mismatches:** {{list or none}}
**Task and diff (conformance review only):** {{task path and git diff command, or none}}

**You may write:** `{{feature folder}}/design-{{domain}}.md` only. In conformance review,
write nothing.

**Constraints:** design only what the intent needs; follow existing patterns unless you
give a reason; do not write product code.

**Return:** `DONE` or `NEEDS_DECISION`; a short summary; contracts provided and consumed;
risks; open decisions with your recommendation. In conformance review, return findings in
the format: severity, `path:line`, design item violated, suggested remedy.
