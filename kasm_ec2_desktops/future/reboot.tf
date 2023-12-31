# reboot.tf

resource "null_resource" "delayed_reboot" {
  count = length(var.ec2_instances)

  triggers = {
    subdomain = var.ec2_instances[count.index]["ec2_Subdomain"]
  }

  provisioner "local-exec" {
    command = "sleep 900"  # Wait for 15 minutes before rebooting
  }

  depends_on = [null_resource.nginx_restart]
}