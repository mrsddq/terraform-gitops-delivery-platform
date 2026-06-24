# Terraform GitOps Delivery Platform

Multi-environment infrastructure delivery platform that shows how Terraform, GitHub Actions, policy checks, and Argo CD fit together in a real DevOps workflow.

## What This Builds

- `dev`, `stage`, and `prod` Terraform environments
- Reusable Terraform modules for network and application platform primitives
- Remote-state backend example with locking
- Pull request workflow for Terraform formatting, validation, plan summary, and security scans
- OPA policy examples for risky infrastructure changes
- Kustomize overlays for Kubernetes deployment promotion
- Argo CD Applications for environment-specific reconciliation

## Delivery Flow

```mermaid
flowchart LR
    PR["Pull Request"] --> CI["GitHub Actions"]
    CI --> Fmt["terraform fmt"]
    CI --> Plan["terraform plan"]
    CI --> Scan["Checkov / tfsec / OPA"]
    Plan --> Comment["Plan Comment"]
    Scan --> Review["Human Review"]
    Review --> Merge["Merge to main"]
    Merge --> Argo["Argo CD Sync"]
    Argo --> Env["dev / stage / prod"]
```

## Repository Layout

```text
terraform/modules/        Reusable infrastructure modules
terraform/envs/           Environment root modules
kubernetes/base/          Shared Kubernetes manifests
kubernetes/overlays/      dev, stage, prod overlays
argocd/applications/      Environment-specific Argo CD Applications
policies/opa/             Policy-as-code examples
scripts/                  Plan comment rendering
tests/                    Static quality checks
```

## Local Validation

```bash
make validate
```

For Terraform formatting:

```bash
make fmt-check
```

## What This Proves

- Can design reusable Terraform without hiding environment differences
- Understands remote state, CI plan review, and policy-as-code gates
- Can map infrastructure delivery into GitOps deployment
- Knows how to structure promotion across `dev`, `stage`, and `prod`
- Documents the review and rollback model clearly

## Safe Demo Mode

The included CI checks do not require cloud credentials. Real plans should run in protected GitHub environments with OIDC-based AWS authentication.
