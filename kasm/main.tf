# main.tf

provider "aws" {
  region = "us-west-2"
}

# Tool versions
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Kasm system properties
resource "aws_instance" "kasm_server" {

  # create a resource 
  for_each = toset(var.kasm_ec2) # for each member of var.kasm_ec2

  # assign current resource a name from key 
  tags = {
    Name = each.key  
  }

  ami           = "ami-04e914639d0cca79a"
  instance_type = "t2.medium"
  key_name      = "Kasm"

  # count = length(var.kasm_ec2) # this does not seem to be needed, discuss with Aaron

  cpu_options = {
    core_count       = 2
    threads_per_core = 1
  }

  ebs_block_device = [
    {
      device_name = "/dev/sdf"
      volume_type = "gp3"
      volume_size = 60
      throughput  = 200
      tags = {
        MountPoint = "/mnt/data"
      }
    }
  ]

  # install Kasm service, after instance is active
  user_data = file("install_kasm.sh")

}
