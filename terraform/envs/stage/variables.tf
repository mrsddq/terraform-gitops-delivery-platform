variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "owner" {
  description = "Resource owner."
  type        = string
}

variable "cost_center" {
  description = "Cost center tag."
  type        = string
}
