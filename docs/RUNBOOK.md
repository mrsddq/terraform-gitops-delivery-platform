# Runbook

## Pull Request Review

1. Confirm Terraform formatting passed.
2. Read the generated plan summary.
3. Review Checkov, tfsec, and OPA results.
4. Confirm blast radius, cost impact, and rollback plan.
5. Merge only after environment owner approval.

## Rollback

- Kubernetes changes: revert the Git commit and let Argo CD reconcile.
- Terraform changes: create a new reviewed plan that restores the previous state.
- State issues: pause applies and inspect the remote state lock before continuing.

## Production Change Rules

- Production applies should use protected GitHub environments.
- AWS access should use OIDC rather than long-lived access keys.
- Emergency changes should receive a follow-up RCA and policy update when relevant.
