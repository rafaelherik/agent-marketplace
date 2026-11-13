---
name: terraform-modules
description: Create, review, refactor, document, and test reusable Terraform modules using provider-neutral best practices. Use when authoring a child module, designing its inputs and outputs, handling provider aliases or version requirements, or changing module resources while preserving existing consumers and state addresses. Also use for module quality reviews and native Terraform tests; not for implementing Terraform providers or routine deployment of an unchanged root configuration.
license: MIT
compatibility: Terraform CLI matching the project's supported versions for executable checks; access to official HTTPS Terraform and provider documentation for version-specific behavior. Follow existing terraform-docs and TFLint configuration when available.
metadata:
  tags:
    - terraform
    - infrastructure
    - modules
---

# Reusable Terraform modules

Build small, cohesive modules with clear contracts and predictable upgrades. Apply
these principles to the provider the project uses; provider-neutral guidance does
not mean building a universal abstraction across clouds.

## 1. Establish the contract

Inspect the module, callers, examples, README, tests, CI, and repository instructions.
Identify what infrastructure the module owns and what callers supply. For an existing
module, record its public inputs, defaults, outputs, provider aliases, and resource
addresses before changing them. Ask only about missing decisions that affect the design.

Resolve the installed Terraform version, `required_version`, tool-version files, and
CI matrix. Read each module's `required_providers` and the consuming root's
`.terraform.lock.hcl` when available. Constraints describe compatibility; a lock file
records selected provider versions, not child-module versions. Distinguish the module's
minimum supported runtime from the newer runtime a test suite might require.

Verify relevant language features and provider arguments against official documentation
for the supported versions, using the host's available documentation tools. If installed,
`context-hub` can help with versioned lookups; it is not a prerequisite. Cite sources
for version-specific decisions. If documentation or execution is unavailable, state
what remains unverified instead of claiming compatibility or passing checks.

## 2. Design or review the module

Use [module design](references/module-design.md) when creating a module or evaluating
its interface, structure, expressions, or documentation.

- Represent a cohesive architectural capability. Prefer shallow composition and
  passing dependencies through inputs to deep nesting or hidden discovery.
- Use explicit types, descriptions, meaningful validations, and intentional defaults.
  Expose outputs that consumers need without leaking unnecessary implementation details.
- Declare provider requirements in the child; keep provider configurations and backends
  in calling roots. Declare aliases and show their explicit mappings in examples.
- Choose stable resource instance keys. Use references for dependencies; add explicit
  `depends_on` only for behavior that references cannot express.
- Follow the repository's layout and naming. Add runnable examples and explain ownership,
  supported versions, inputs, outputs, and trade-offs in the README.

For reviews, report concrete findings with file/line references, impact on consumers,
and a suggested fix. Distinguish correctness or compatibility defects from preferences;
do not turn every convention into a mandatory rewrite.

## 3. Preserve upgrade paths

Read [compatibility and refactoring](references/compatibility.md) before changing
addresses, public interfaces, provider requirements, or module boundaries.

Compare old and new contracts. Use explicit `moved` mappings for supported address
changes, retain historical mappings, and document migrations and intentional breaking
changes. An address move does not prove that changed resource arguments avoid replacement:
inspect a representative upgrade plan when the environment permits it.

## 4. Verify the behavior

Follow [testing](references/testing.md) to select checks appropriate to the change and
the project's Terraform version. Start with formatting and validation, then test the
public behavior, invalid inputs, and important optional branches. Use the repository's
existing linting and documentation tools.

Inspect test run commands and provider configuration before executing `terraform test`:
its default run command is `apply`. Prefer explicit plan runs and supported mocks for
fast contract tests; identify real-provider integration tests and their environment
requirements separately. A plan using real providers can still need credentials and
make remote reads.

## 5. Summarize the result

Keep the handoff proportional: describe the contract changes, compatibility or migration
implications, and exact checks run with their results. Name skipped checks and the missing
prerequisite. Link the relevant examples or migration notes so a consumer can use the
module without reverse-engineering it.
