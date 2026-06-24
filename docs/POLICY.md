# Policy Model

The OPA examples are intentionally readable so they can be discussed in interviews and extended in real teams.

## Example Policies

- Deny public S3 bucket ACLs.
- Require cost-center and owner tags.
- Flag public security group ingress outside approved ports.
- Require production changes to include explicit review metadata.

## Where Policy Runs

Policy should run in pull requests before infrastructure changes are applied. Blocking gates belong before `terraform apply`, while advisory checks can be reported as comments.
