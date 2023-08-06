# _main.tf

# Oregon region
provider "aws" {
  region = "us-west-2"
}

# tool versions
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# construct data
locals {
  # define ec2 instance plan
  ec2_instances = [
    for i in range(var.instances_start,  var.instances_start + var.instances_count) : {
      ec2_Name      = "${var.instances_prefix}${i}.${var.domain_tag}"
      ec2_Subdomain = lower("${var.instances_prefix}")
      ec2_Domain    = lower("${var.instances_prefix}${i}.${var.domain}")
    }
  ]
}

# provision ec2 installation scripts
data "template_file" "ec2_install" {
  count = length(local.ec2_instances)
  template = file("${path.module}/ec2_install.sh.tpl")

  vars = {
    SUBDOMAIN = local.ec2_instances[count.index]["ec2_Subdomain"]
    DOMAIN    = local.ec2_instances[count.index]["ec2_Domain"]
    EMAIL     = var.email
  }
}

