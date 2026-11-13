# Terraform modules

[Back to registry](../../README.md#available-skills)

The `terraform-modules` skill helps agents create, review, refactor, document, and test
reusable Terraform modules. Its provider-neutral guidance follows HashiCorp's module
design practices and adapts to the consuming repository's conventions and supported
Terraform/provider versions.

See the [skill instructions](../../skills/terraform-modules/SKILL.md),
[module design](../../skills/terraform-modules/references/module-design.md),
[compatibility](../../skills/terraform-modules/references/compatibility.md), and
[testing guidance](../../skills/terraform-modules/references/testing.md).

## Install

Follow the [registry installation instructions](../../README.md#install), selecting
`terraform-modules` and a published tag that contains it. For local development, use
the [directory-source configuration](../../README.md#develop-and-validate) with:

```yaml
resources:
  development:
    include: [skill/terraform-modules]
```

Run `agent-marketplace sync` from the consuming repository. Installation provides
instructions, references, and evaluation cases; configure the toolchain separately.

## Runtime prerequisites

- Install the Terraform CLI version selected by the consuming project. Verify it with
  `terraform version`. Reviews can proceed without the CLI, but execution checks will
  be reported as unverified.
- Native Terraform tests require 1.6+; provider mocks require 1.7+. The skill distinguishes
  test-runner requirements from the module's minimum supported Terraform version.
- Enable the host's documentation fetch/browser tools for official Terraform and
  provider documentation. The `context-hub` skill can complement lookups when installed.
- Use TFLint and `terraform-docs` when the repository already configures them. There is
  no mandatory MCP server or cloud-specific dependency for this skill.
- Provider installation can need network access. Tests using real providers may need
  credentials; apply-based tests can provision infrastructure and require cleanup.

## Example requests

- "Create a reusable module with typed inputs, useful outputs, a minimal example, and
  tests for its public contract. Follow this repository's provider and version policy."
- "Review this module for composability, provider handling, input validation, and
  compatibility problems. Give concrete findings with file references."
- "Refactor these indexed resources to stable keys. Preserve existing consumers and
  explain the address mappings and upgrade verification."

## Evaluation cases

The skill's `evals/` directory contains repeatable authoring, review, and refactoring
scenarios with expected outcomes and graders. These evaluate agent behavior; the
registry's existing validator separately checks metadata, bundled links, and installation
across supported harnesses.
