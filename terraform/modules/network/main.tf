resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name        = "${var.name}-${var.environment}"
    Environment = var.environment
  })
}

resource "aws_subnet" "private" {
  count = 2

  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.cidr_block, 4, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(var.tags, {
    Name        = "${var.name}-${var.environment}-private-${count.index + 1}"
    Environment = var.environment
    Tier        = "private"
  })
}

data "aws_availability_zones" "available" {
  state = "available"
}
