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

# create AWS EC2 instance
resource "aws_instance" "kasm_server" {

  # repeat for each var.kasm_ec2
  for_each = toset(var.kasm_ec2)

  # assign current "each.key" a tag, tags are a list property
  tags = {
    name = each.key  
  }

  # EC2 key-value properties
  ami           = "ami-04e914639d0cca79a"  # ubuntu predefined image
  instance_type = "t2.medium"
  key_name      = "Kasm"

  # EC2 cpu properties are lists
  cpu_options = {
    core_count       = 2
    threads_per_core = 1
  }

  # EC2 storage properties are lists
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

  # For EC2, elastic ip's are an external resource
  # kasm_eip is elastic ip resources in aws_eip pool
  resource "aws_eip" "kasm_eip" { 
    count = length(var.kasm_ec2)

    instance = aws_instance.kasm_server[count.index].id
  }

  # Security group
  vpc_security_group_ids = [aws_security_group.kasm_sg.id]

  # For EC2/AMI, install Kasm resources for Ubuntu
  user_data = file("install_kasm.sh")

  # Nginx provisioning
  provisioner "file" {
    source      = "nginx.conf"  
    destination = "/etc/nginx/sites-available/nginx.conf" 
  }

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

# Define the template for your nginx configuration
data "template_file" "nginx_conf_template" {
  template = file("${path.module}/nginx.conf.tpl")

  vars = {
    subdomain = replace(var.kasm_ec2[count.index], "\\..*$", "")
  }
}

# Create an nginx.conf file using the rendered template
resource "null_resource" "nginx_conf" {
  count = length(var.kasm_ec2)

  triggers = {
    template = data.template_file.nginx_conf_template.rendered
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.nginx_conf_template.rendered}' > /tmp/nginx.conf.tpl"
  }

  provisioner "file" {
    source      = "/tmp/nginx.conf.tpl"
    destination = "/etc/nginx/sites-available/nginx.conf"
  }
}
