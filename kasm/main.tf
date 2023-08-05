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

data "template_file" "install_kasm_script" {
  count = length(var.kasm_instances)
  template = file("${path.module}/install_kasm.sh.tpl")

  vars = {
    SUBDOMAIN = var.kasm_instances[count.index]["ec2_Subdomain"]
    DOMAIN    = var.kasm_instances[count.index]["ec2_Domain"]
    EMAIL     = var.email
  }
}

# create AWS EC2 instances
resource "aws_instance" "kasm_server" {
  count = length(var.kasm_instances)

  tags = {
    Name   = var.kasm_instances[count.index]["ec2_Name"]
    Domain = var.kasm_instances[count.index]["ec2_Domain"]
  }

  # EC2 key-value properties
  ami           = "ami-03f65b8614a860c29"  # ubuntu predefined image
  instance_type = "t2.medium"
  key_name      = "kasm"

  # EC2 storage properties are lists
  ebs_block_device {
    device_name = "/dev/sda1"
    volume_type = "gp3"
    volume_size = 60
    tags = {
      MountPoint = "/mnt/data"
    }
  }

  # Security group
  vpc_security_group_ids = [aws_security_group.kasm_sg.id]

  # For EC2/AMI, install Kasm resources for Ubuntu
  user_data = data.template_file.install_kasm_script[count.index].rendered
}

# Elastic ip's
resource "aws_eip" "kasm_eip" {
  count = length(aws_instance.kasm_server)

  instance = aws_instance.kasm_server[count.index].id
}

# Security Group for Kasm instances
resource "aws_security_group" "kasm_sg" {
  name_prefix = "kasm_sg_"

  # incoming network traffic rules
  
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

  # outbound network traffic rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
}

