# Testing modules

## Establish the toolchain

Read the module's supported Terraform versions, test files, CI commands, and tool
configuration before selecting checks. Use the project's pinned tools where available.
If a tool is missing, report the skipped check and prerequisite; do not report a pass.

Native `.tftest.hcl` tests require Terraform 1.6+. Provider mocks and overrides require
Terraform 1.7+. A test runner can be newer than the minimum supported module runtime;
check minimum-runtime compatibility separately. For older runtimes, use existing test
tools and example-root validation rather than inserting unsupported test syntax.

## Static checks

From the module directory, the usual starting sequence is:

```bash
terraform fmt -check -recursive
terraform init -backend=false -input=false
terraform validate
```

During implementation, use `terraform fmt -recursive` to fix formatting before the check.
Initialization installs referenced modules and providers, can require network access,
and may create a local lock file. Respect existing locks and inspect resulting changes.
Validation checks syntax and internal consistency, not cloud API behavior or a deployment
plan. A child requiring provider aliases may need a small calling root with the mappings
to validate it in context; do not insert provider configurations into the child to make
standalone validation pass. Initialize and validate examples in their own directories.

Run configured TFLint rules and documentation checks when present. Use existing
`terraform-docs` configuration and markers rather than regenerating an entire README
with guessed options. These tools supplement Terraform's checks.

## Contract tests

Test observable behavior: important defaults, caller overrides, optional branches,
output shapes, and rejection of invalid combinations. Assert domain invariants rather
than merely repeating expressions from the implementation. Test meaningful boundary
cases without retesting Terraform's own type system.

Use explicit `command = plan` where assertions can be evaluated at plan time. This
small example assumes the module defines `replica_count`, rejects non-positive values,
and exposes its effective count as an output:

```hcl
variables {
  replica_count = 2
}

run "accepts_requested_count" {
  command = plan

  assert {
    condition     = output.replica_count == 2
    error_message = "The module must honor the requested replica count."
  }
}

run "rejects_zero_count" {
  command = plan

  variables {
    replica_count = 0
  }

  expect_failures = [var.replica_count]
}
```

`expect_failures` targets user-defined custom conditions, not arbitrary provider errors
or type mismatches. Prefer one failing input condition per run so an early failure does
not conceal another. Assertions depending on computed values may need explicit mock
values or an apply-based test instead of a plan-only test.

On Terraform 1.7+, use `mock_provider` and overrides when testing module logic without
remote APIs. Supply concrete mock values where assertions depend on them. Mocks do not
prove real-provider behavior, authentication, or remote API compatibility, and provider
schemas still need to be installed. Map provider aliases in tests just as callers do.

## Integration and upgrade tests

Inspect the entire test file, including setup runs and alternate modules: a `run` with
no `command` defaults to `apply`. Test files can mix mocked and real providers. Even
`command = plan` with real providers can refresh data and require credentials.

For integration tests that provision infrastructure, use the project's designated test
environment and document required credentials, cost-relevant resources, and cleanup.
Terraform uses test-specific state and attempts teardown, but external effects and
failed cleanup can remain. Inspect the test result and any cleanup instructions.

For migrations, use an old-version fixture and representative state to exercise the
upgrade to the changed module. Confirm expected address moves and investigate unexpected
destruction or replacement. Fresh deployments do not demonstrate upgrade compatibility.
See [compatibility](compatibility.md) for mapping constraints and historical moves.

## Report evidence

List the commands, Terraform/provider versions, and outcomes. Separate formatting and
validation from mocked contract tests, real-provider integration tests, and upgrade
plans. Explain missing credentials, unsupported tool versions, or unavailable state
when those prevent checks; do not imply skipped checks succeeded.

## Official sources

- [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)
- [Provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking)
- [terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
- [terraform fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt)
- [Custom conditions](https://developer.hashicorp.com/terraform/language/expressions/custom-conditions)
