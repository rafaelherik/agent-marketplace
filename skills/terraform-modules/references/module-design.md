# Module design

## Boundaries and composition

Design around one capability whose resources have a shared lifecycle and ownership.
A module should add useful defaults, policy, or composition rather than merely rename
every argument of a single resource. A small wrapper can still be justified when it
enforces a meaningful, documented organizational contract.

Keep module trees relatively flat. Accept dependencies such as network identifiers or
small typed objects from the caller instead of making the module create or discover
everything. Let the caller choose whether a dependency is new or existing. Avoid a
collection of boolean switches that turns one module into unrelated architectures.

## Layout

Use the standard structure, adapted to existing repository conventions:

```text
module/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── README.md
├── examples/
│   └── minimal/
└── tests/
    └── contract.tftest.hcl
```

Terraform combines the `.tf` files in a directory; file names are organizational, not
execution order. Split a growing `main.tf` by coherent responsibility when helpful.
Use `modules/` for meaningful nested modules, documenting which are public and supported.
Create files with useful content rather than empty boilerplate.

Examples are runnable root configurations: show provider configuration and required
alias mappings there, with a local source pointing to the module under development.
Keep example values illustrative and free of credentials. Each independently runnable
root needs its own initialization and validation.

## Inputs and outputs

- Give variables explicit types and descriptions that explain meaning, units, constraints,
  and the effects of omission. Prefer small, meaningful object types to `any` or an
  unstructured bag of settings. Use `any` only when truly passing opaque data through.
- Choose defaults only where they are valid and unsurprising for supported callers.
  Required decisions should remain required inputs. Treat `null`, omission, empty strings,
  and empty collections deliberately; they are not interchangeable.
- Use `nullable = false` when null has no defined meaning. Optional object attributes
  with defaults require Terraform 1.3+; verify more advanced validation against the
  supported runtime before using it.
- Validate module-specific invariants with actionable errors. Use preconditions or
  postconditions for assumptions involving resources when the runtime supports them.
  Do not use non-blocking `check` assertions as enforcement of mandatory invariants.
- Mark sensitive inputs and outputs appropriately. `sensitive` redacts ordinary display;
  it does not prevent persistence in state. Avoid embedding secrets in defaults or examples.
- Return documented values needed for composition, such as identifiers or endpoint
  objects with stable fields. Avoid exposing entire provider resources as a public API
  unless that coupling is intentional. Reference resource attributes in outputs so
  Terraform retains the relevant dependency relationship.

## Providers and versions

Every module declares its own `required_providers`, including source addresses and
minimum versions needed for the actual features used. Provider requirements are not
inherited. Prefer minimum constraints in reusable modules; add upper bounds only when
there is a documented incompatibility. Root configurations select and lock the concrete
provider versions for a deployment.

Keep `provider` and `backend` blocks out of reusable child modules. Provider configurations
belong to roots; test files may also configure providers for test runs. Default provider
configurations can be inherited, but aliases require `configuration_aliases` in the child
and explicit `providers` mappings at the call site. A variable cannot dynamically select
a provider configuration. Use separate module calls for different provider mappings.

Set `required_version` to a justified Terraform minimum and honor the repository's
documented support policy. Do not automatically raise the module runtime merely to use
newer test tooling. See [compatibility](compatibility.md) for lock files and upgrades.

## Expressions and resource identity

- Prefer readable names and expressions. Use locals for meaningful derived values or
  normalization, not aliases for every input.
- Choose `for_each` for resources with caller-defined identities and stable keys known
  at plan time. Use `count` for truly positional interchangeable instances or a simple
  optional singleton. Reordering a list used by `count` can change resource identities.
- Do not use generated IDs, sensitive values, or unstable values as instance keys.
  A map with caller-known keys can contain values that are unknown until apply.
- Use ordinary resource references to express dependencies. Broad module-level
  `depends_on` can make unrelated values unknown at plan time and produce noisy plans.
- Prefer direct expressions to unnecessary `dynamic` blocks. Reserve `try`/`can` for
  intentional normalization or validation, rather than masking broken assumptions.
- Avoid provisioners when a provider resource or external build/configuration workflow
  expresses the lifecycle better. Explain any necessary provisioner or lifecycle override;
  broad `ignore_changes` is not a substitute for deciding ownership.

## Documentation

Explain the module's purpose, ownership boundary, prerequisites, supported versions,
provider aliases, inputs/defaults, outputs, and a minimal usage example. Describe important
optional behavior and migration requirements. Follow an existing `terraform-docs` config
and generated-section markers; generated tables complement architectural explanations.

## Official sources

- [Creating modules](https://developer.hashicorp.com/terraform/language/modules/develop)
- [Standard module structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure)
- [Module composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)
- [Providers within modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers)
- [Style guide](https://developer.hashicorp.com/terraform/language/style)
- [Optional object attributes](https://developer.hashicorp.com/terraform/language/expressions/type-constraints#optional-object-type-attributes)
- [Sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)

Use the documentation version selector for a project's supported Terraform version.
