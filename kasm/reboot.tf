# reboot.tf

# Use the same provider configuration as in your main.tf
provider "aws" {
  region = "us-west-2"
}

# Reboot EC2 instances after provisioning
resource "aws_instance" "reboot_instances" {
  count = length(var.kasm_ec2)

  depends_on = [
    aws_instance.kasm_server[count.index],
    aws_route53_record.kasm_dns[count.index],
    null_resource.nginx_conf[count.index]
  ]

  instance_ids = [aws_instance.kasm_server[count.index].id]

  provisioner "remote-exec" {
    inline = [
      "sudo reboot",
    ]
  }
}
