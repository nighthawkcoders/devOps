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
  # define kasm ec2 instance plan
  kasm_instances = [
    for i in range(var.starting_instance_number, var.starting_instance_number + var.kasm_instance_count) : {
      ec2_Name      = "${var.instance_name}${i}.${var.domain_tag}"
      ec2_Subdomain = lower("${var.instance_name}")
      ec2_Domain    = lower("${var.instance_name}${i}.${var.domain}")
    }
  ]
}

# construct kasm ec2 installation scripts
data "template_file" "ec2_install" {
  count = length(local.kasm_instances)
  template = file("${path.module}/ec2_install.sh.tpl")

  vars = {
    SUBDOMAIN = local.kasm_instances[count.index]["ec2_Subdomain"]
    DOMAIN    = local.kasm_instances[count.index]["ec2_Domain"]
    EMAIL     = var.email
  }
}

