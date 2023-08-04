# reboot.tf

# Reboot EC2 instances after provisioning
resource "aws_instance" "reboot_instances" {
  count = length(var.kasm_ec2)

  instance_ids = [aws_instance.kasm_server[count.index].id]

  provisioner "remote-exec" {
    inline = [
      "sudo reboot",
    ]
  }
}
