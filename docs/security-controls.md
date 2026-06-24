# Security Controls

## Implemented

- CI Terraform formatting and static tests.
- Checkov soft scan in GitHub Actions.
- OPA policy examples for public ingress and required tags.
- Environment separation for `dev`, `stage` and `prod`.
- Production Argo CD app avoids automated sync by default.

## Recommended Production Additions

- GitHub OIDC to AWS.
- Required reviewers for production environment.
- TFLint, tfsec or Checkov as blocking gates.
- Signed commits or protected branches.
- Secret scanning and dependency scanning.
- Conftest against real Terraform plan JSON.

## Security Review Questions

- Which policy blocks public ingress?
- Which environments can auto-apply?
- How are production approvals enforced?
- Where is state stored and locked?
- How are tags and ownership enforced?
