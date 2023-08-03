
provider "aws" {
  region = "us-west-2"
}


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "kasm_server" {
  ami           = "ami-04e914639d0cca79a"
  name          = each.value
  for_each      = toset(var.kasm_ec2)
  instance_type = "t2.medium"
  key_name      = "Kasm"

  user_data = <<-EOT
   #!/bin/bash
   echo "Hello Terraform!"
 EOT
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

  tags = {
    Name = "kasm"
  }
}
