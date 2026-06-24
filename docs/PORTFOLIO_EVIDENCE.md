# Portfolio Evidence

This repo demonstrates how infrastructure changes can move through CI validation, policy review and GitOps promotion.

## Verified Locally

```bash
python -m unittest discover -s tests
python scripts/render_plan_comment.py --sample
terraform fmt -recursive -check terraform
```

Sample plan-comment output:

```markdown
## Terraform Plan Summary

| Action | Count |
| --- | ---: |
| Create | 1 |
| Update | 1 |
| Delete | 1 |
| Replace | 0 |
| No-op | 1 |
```

## Reviewer Evidence

| Evidence | Location | What it proves |
|---|---|---|
| CI badge | `README.md` | Terraform formatting, tests and Checkov soft scan run in CI. |
| Environments | `terraform/envs/` | Separate `dev`, `stage` and `prod` root modules. |
| Modules | `terraform/modules/` | Reusable network and platform primitives. |
| Policies | `policies/opa/terraform.rego` | Policy-as-code guardrail examples. |
| GitOps overlays | `kubernetes/overlays/` | Environment promotion through Kustomize. |
| Argo CD apps | `argocd/applications/` | GitOps reconciliation per environment. |
