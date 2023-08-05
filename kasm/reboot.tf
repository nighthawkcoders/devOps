# reboot.tf

resource "null_resource" "reboot_instances" {
  for_each = aws_instance.kasm_server

  triggers = {
    instance_id = each.value.id
  }

  provisioner "local-exec" {
    command = "aws ec2 reboot-instances --instance-ids ${each.value.id}"
  }

  depends_on = [null_resource.nginx_restart]  # Make sure this is correct based on your dependencies
}