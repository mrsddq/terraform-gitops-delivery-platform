# Runbook

## Prerequisites

- Terraform `>= 1.6`
- AWS authentication through SSO, assumed role or CI OIDC
- Remote state backend for shared use
- Environment values reviewed before apply

## Validate

```bash
make test
make lint
python scripts/render_plan_comment.py --sample
```

## Deploy

```bash
make deploy ENV=dev CONFIRM_DEPLOY=true
```

Use protected approvals before `stage` and `prod`.

## Destroy

```bash
make destroy ENV=dev CONFIRM_DEPLOY=true
```

## Rollback

- Terraform rollback must be a new reviewed plan.
- Kubernetes rollback should use Git revert and Argo CD sync.
- Production rollback requires owner approval and incident/change record.
