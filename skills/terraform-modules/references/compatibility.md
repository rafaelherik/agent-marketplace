# Compatibility and refactoring

## Identify the supported contract

Before editing an existing module, compare its released interface with the proposed one:

- Input names, types, defaults, null handling, and validation constraints.
- Output names, value shapes, sensitivity, and semantics.
- Provider sources, version requirements, and configuration aliases.
- Resource and module addresses, including `count` indices and `for_each` keys.
- Resource arguments or lifecycle behavior that could cause replacement or change ownership.

An additional required input, a changed default, a removed output, or tighter validation
can break consumers even when Terraform syntax remains valid. Document these changes
using the repository's release conventions, with upgrade examples where needed.

## Versions and dependency locks

Record both declared compatibility and versions actually tested. A successful run on
the newest Terraform or provider does not establish compatibility with the declared
minimum. Exercise the minimum and a representative current supported combination when
changing version-sensitive features, using existing CI conventions where possible.

The consuming root's `.terraform.lock.hcl` records selected provider versions and
checksums. Terraform does not use a child module's lock file to constrain the caller,
and lock files do not lock remote module versions. Keep root lock files under the
repository's established policy; a module repository may retain its own lock for local
tests, but do not advertise that as a lock on consumers.

Registry module dependencies use `version` constraints; Git module sources use a `ref`
in the source URL. Follow the project's reproducibility policy and prefer explicit,
reviewable release references over an implicit moving branch. Do not add a `version`
argument to a Git or local module source. Avoid `terraform init -upgrade` during routine
validation because it changes dependency selection.

## Preserve resource addresses

Use declarative `moved` blocks for supported address refactors (Terraform 1.1+). Place
them in the module that owns the relevant addresses. For example, a module using the
built-in `terraform_data` resource (Terraform 1.4+) can rename a resource with:

```hcl
moved {
  from = terraform_data.old
  to   = terraform_data.current
}
```

For a conversion from `count` to stable keys, map each previous instance explicitly:

```hcl
moved {
  from = terraform_data.item[0]
  to   = terraform_data.item["primary"]
}

moved {
  from = terraform_data.item[1]
  to   = terraform_data.item["secondary"]
}
```

These are illustrative mappings, not a template to apply blindly. If each caller has
different index-to-key assignments, obtain the actual mapping or provide a caller-specific
migration procedure. `moved` blocks cannot be generated using `for_each` or `count`.
Never guess which existing object belongs to a new key.

Retain historical moves, including chained moves, so callers can skip intermediate
releases. Removing a historical move can break upgrades. Moving between module boundaries
requires checking the supported move rules and placing the mapping at the appropriate
common scope; changing resource types also requires explicit provider support.

For Terraform versions without the required move support, document a precise, coordinated
state migration instead of silently raising the runtime minimum. Treat imperative state
commands as an environment-specific migration, not a routine code-formatting operation.

## Verify upgrades

Use a representative caller and existing state to compare before/after plans. Confirm
that expected moves are recognized, and inspect create, destroy, and replacement actions.
Changing addresses and changing replacement-sensitive arguments at the same time can
still replace resources despite a correct move. Avoid describing a refactor as zero
replacement based solely on `validate` or a fresh-state plan.

If representative state or credentials are unavailable, inspect the mappings statically
and state that upgrade behavior is unverified. Describe which plan the consumer needs
to run. Include changes to aliases, dependency requirements, public inputs, and outputs
in the migration notes even when resource addresses are preserved.

## Official sources

- [Refactoring modules](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
- [Provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)
- [Dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
- [Module sources](https://developer.hashicorp.com/terraform/language/modules/sources)
- [Terraform compatibility promises](https://developer.hashicorp.com/terraform/language/v1-compatibility-promises)
- [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
