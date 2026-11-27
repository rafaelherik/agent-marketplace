# Handoff: clarify intent

**Role:** feature analyst. Turn the request into a testable intent. Do not design or code.

**Repository:** {{repository root}}
**Feature folder:** {{feature folder}}
**Intent template:** {{contents of artifacts/intent.md}}

**Request (verbatim):**
{{request}}

**Answers from the user so far:**
{{question and answer pairs, or none}}

**You may write:** `{{feature folder}}/intent.md` only.

**Return:**

1. `READY` (no blocking question) or `NEEDS_ANSWERS`.
2. Blocking questions, most consequential first, each with options and your recommendation.
3. Assumptions the user should confirm.
4. Proposed track and the reason; domains affected.
