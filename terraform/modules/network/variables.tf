variable "name" {
  description = "Name prefix for network resources."
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "tags" {
  description = "Common tags."
  type        = map(string)
  default     = {}
}
