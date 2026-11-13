---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Review this reusable child module before we publish its next version. Give prioritized
findings with locations, impact, and practical fixes in response.md. Do not provision
anything or rewrite the module. We support Terraform 1.6 and our test runner is also 1.6.
No cloud credentials or prior state are available.

main.tf:
```hcl
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "= 5.0.0" }
  }
  backend "s3" { bucket = "company-state" }
}

provider "aws" { region = "us-east-1" }

variable "names" { type = list(string) }
variable "secret" {
  type      = string
  sensitive = true
}

resource "aws_ssm_parameter" "entry" {
  count = length(var.names)
  name  = var.names[count.index]
  type  = "SecureString"
  value = var.secret
}

output "entries" {
  value     = aws_ssm_parameter.entry
  sensitive = true
}
```

tests/smoke.tftest.hcl:
```hcl
mock_provider "aws" {}
run "smoke" {}
```

README.md says: "Sensitive values never enter state. Our module lock file pins the
provider version for all callers. The smoke test proves AWS accepts this configuration."
Existing callers pass names in different orders and consume entries as a list.
