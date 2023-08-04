# main.tf

locals {
  kasm_ec2 = [for sub in var.subdomain : "${sub}.${var.domain_tag}"]
}

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

# create AWS EC2 instance
resource "aws_instance" "kasm_server" {

  # repeat for each kasm_ec2
  for_each = toset(local.kasm_ec2)

  # assign current "each.key" a tag, tags are a list property
  tags = {
    name = each.key  
  }

  # EC2 key-value properties
  ami           = "ami-04e914639d0cca79a"  # ubuntu predefined image
  instance_type = "t2.medium"
  key_name      = "Kasm"

  # EC2 storage properties are lists
  ebs_block_device {
    device_name = "/dev/sdf"
    volume_type = "gp3"
    volume_size = 60
    throughput  = 200
    tags = {
      MountPoint = "/mnt/data"
    }
  }

  # Security group
  vpc_security_group_ids = [aws_security_group.kasm_sg.id]

  # For EC2/AMI, install Kasm resources for Ubuntu
  user_data = file("install_kasm.sh")

}

# Elastic ip's are 
resource "aws_eip" "kasm_eip" {
  for_each = aws_instance.kasm_server

  instance = each.value.id
}

# Security Group for Kasm instances
resource "aws_security_group" "kasm_sg" {
  name_prefix = "kasm_sg_"

  # incoming network traffic rules follow
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH traffic"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP traffic"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS traffic"
  }

}

