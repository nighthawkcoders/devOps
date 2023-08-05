# ec2.tf

module "security_group" {
  source = "./security-group"
}

# create AWS EC2 instances
resource "aws_instance" "kasm_server" {
  count = length(local.kasm_instances) # aws_instance iterator

  # assign Meta data
  tags = {
    Name   = local.kasm_instances[count.index]["ec2_Name"]  # Name tag for AWS console
    Domain = local.kasm_instances[count.index]["ec2_Domain"]
  }

  # assign EC2 key-value properties
  ami           = "ami-03f65b8614a860c29"  # ubuntu predefined image
  instance_type = "t2.medium"
  key_name      = "${var.key_pair}"

  # assign EC2 storage properties
  ebs_block_device {
    device_name = "/dev/sda1"
    volume_type = "gp3"
    volume_size = 60
    tags = {
      MountPoint = "/mnt/data"
    }
  }

  # create reference to a Security group, see security-group/main.tf
  vpc_security_group_ids = [module.security_group.kasm_sg_id]

  # file provision and assign System setup script, see ec2_install.sh.tpl
  user_data = data.template_file.ec2_install[count.index].rendered
}