resource "aws_security_group" "app_ingress" {
  name        = "${var.name}-${var.environment}-app-ingress"
  description = "Ingress boundary for application traffic."
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP ingress from load balancer"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    description = "Outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name        = "${var.name}-${var.environment}-app-ingress"
    Environment = var.environment
  })
}
