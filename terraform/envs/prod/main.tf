terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  tags = {
    Project     = "terraform-gitops-delivery-platform"
    Environment = "prod"
    Owner       = var.owner
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
    ChangeTier  = "protected"
  }
}

module "network" {
  source      = "../../modules/network"
  name        = "delivery"
  environment = "prod"
  cidr_block  = "10.70.0.0/16"
  tags        = local.tags
}

module "app_platform" {
  source      = "../../modules/app_platform"
  name        = "delivery"
  environment = "prod"
  vpc_id      = module.network.vpc_id
  tags        = local.tags
}
