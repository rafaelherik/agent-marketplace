---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Refactor this released module from count to for_each using the existing names as keys.
We support Terraform 1.4. Preserve the names input and ids output contract for callers,
including output ordering. Names are unique, but each caller has a different ordering.
The example caller uses ["api", "worker"]. We have no access to existing state today.
Provide the revised .tf files and migration notes in response.md; do not claim to have
verified an upgrade against real state.

```hcl
terraform { required_version = ">= 1.4.0" }

variable "names" { type = list(string) }

resource "terraform_data" "entry" {
  count = length(var.names)
  input = var.names[count.index]
}

output "ids" { value = terraform_data.entry[*].id }

moved {
  from = terraform_data.old_entry
  to   = terraform_data.entry
}
```

I was thinking we could generate moved blocks with for_each or simply use the example
caller's mappings for everyone. Please handle whichever is appropriate for consumers.
