# Incident Response

## Example Incidents

| Incident | Detection | Mitigation |
|---|---|---|
| Terraform apply partially fails | CI/apply logs and state lock | Stop further applies, inspect state, fix and re-plan |
| Bad production overlay | Argo CD degraded app | Revert overlay commit |
| Unsafe security group change | Policy or reviewer detection | Block merge or apply corrective plan |
| State lock stuck | Terraform lock error | Confirm no active apply, then release lock with change record |

## RCA Notes

- Capture PR, plan summary and commit SHA.
- Record environment, module and affected resources.
- Identify missing policy or review step.
- Add policy, test or module guardrail to prevent recurrence.
