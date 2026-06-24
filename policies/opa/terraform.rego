package terraform.guardrails

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.type == "ingress"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  not approved_public_port(resource.change.after.from_port)
  msg := sprintf("public ingress is not approved for %s", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  tags := resource.change.after.tags
  not tags.Owner
  msg := sprintf("missing Owner tag on %s", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  tags := resource.change.after.tags
  not tags.CostCenter
  msg := sprintf("missing CostCenter tag on %s", [resource.address])
}

approved_public_port(port) {
  port == 80
}

approved_public_port(port) {
  port == 443
}
