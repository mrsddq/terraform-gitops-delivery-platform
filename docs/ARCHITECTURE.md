# Architecture

This repo models a delivery platform where Terraform owns cloud infrastructure and Argo CD owns Kubernetes reconciliation.

## Environment Roots

Each environment root under `terraform/envs` uses the same modules with different inputs. That gives reviewers a consistent shape while preserving production-specific scale and guardrails.

## Promotion Model

Application manifests start in `kubernetes/base` and are customized with overlays. Argo CD Applications point to each overlay, making deployment state visible and auditable.

## Security Gates

CI is expected to run:

- Terraform formatting and validation
- Plan generation and PR comments
- Checkov and tfsec scans
- OPA policy checks for organization-specific rules

The sample workflow runs safe checks without credentials. A production version should add OIDC-based AWS authentication and protected environments.
