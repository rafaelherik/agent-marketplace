---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Create a small reusable deployment-catalog module for an offline training repository.
It represents named deployment records using Terraform's built-in terraform_data
resource, one per caller-defined key. Accept a map of objects with a required nonempty
owner and an optional environment defaulting to "dev"; permit only dev, staging, or prod.
Expose the effective records as an output map keyed the same way. Include a runnable
minimal example, README, and tests for defaults, overrides, and invalid inputs.

The module must remain usable on Terraform 1.4; CI can run tests on a newer version.
Use no external providers or cloud services. Verify what you can with the installed CLI
and report the actual version and checks. Write the module files and a response.md summary.
