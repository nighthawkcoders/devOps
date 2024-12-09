# ec2.tf

# create AWS EC2 instances
resource "aws_instance" "ec2_server" {
    count = length(local.ec2_instances) # aws_instance iterator

    # assign Meta data
    tags = {
        Name   = local.ec2_instances[count.index]["ec2_Name"]  # Name tag for AWS console
        Domain = local.ec2_instances[count.index]["ec2_Domain"]
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

    # create reference to a Security group, see security.tf
    vpc_security_group_ids = [aws_security_group.web_sg.id]

    # file provision and assign System setup script, see ec2_install.sh.tpl
    user_data = element(local.ec2_install, count.index)
}