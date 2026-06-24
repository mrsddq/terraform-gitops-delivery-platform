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
    Environment = "stage"
    Owner       = var.owner
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
  }
}

module "network" {
  source      = "../../modules/network"
  name        = "delivery"
  environment = "stage"
  cidr_block  = "10.60.0.0/16"
  tags        = local.tags
}

module "app_platform" {
  source      = "../../modules/app_platform"
  name        = "delivery"
  environment = "stage"
  vpc_id      = module.network.vpc_id
  tags        = local.tags
}
