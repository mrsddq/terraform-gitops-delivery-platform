output "app_ingress_security_group_id" {
  description = "Security group used by the app ingress layer."
  value       = aws_security_group.app_ingress.id
}
