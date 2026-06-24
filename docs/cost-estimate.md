# Cost Estimate

This repo models infrastructure delivery patterns. Actual costs depend on modules and environment inputs.

## Cost Drivers

| Area | Cost driver | Control |
|---|---|---|
| VPC | NAT gateway and data processing | Use sandbox-friendly NAT design |
| Application platform | Security groups and attached services | Keep examples minimal |
| CI | Action minutes and scans | Keep scans scoped |
| Kubernetes overlays | Cluster resources | Use small replica counts by environment |

## Guardrails

- Require `Owner`, `CostCenter` and `Environment` tags.
- Use remote state with locking.
- Run plan comments before apply.
- Use AWS Budgets for live environments.
- Destroy demo environments after review.
