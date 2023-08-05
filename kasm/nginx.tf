# nginx.tf

# Define the nginx configuration file template
data "template_file" "nginx_conf_template" {
  count = length(var.kasm_instances)
  template = file("${path.module}/nginx.conf.tpl")

  vars = {
    subdomain = var.kasm_instances[count.index]["ec2_Subdomain"]
    domain    = var.kasm_instances[count.index]["ec2_Domain"]
  }
}

# Create the nginx configuration file from the template
resource "local_file" "nginx_conf" {
  count    = length(var.kasm_instances)
  filename = "/etc/nginx/sites-available/${var.kasm_instances[count.index]["ec2_Subdomain"]}.conf"
  content  = data.template_file.nginx_conf_template[count.index].rendered
}

# Create a symbolic link for the enabled sites
resource "null_resource" "nginx_symlink" {
  count = length(var.kasm_instances)

  triggers = {
    subdomain = var.kasm_instances[count.index]["ec2_Subdomain"]
  }

  provisioner "local-exec" {
    command = "ln -s /etc/nginx/sites-available/${var.kasm_instances[count.index]["ec2_Subdomain"]}.conf /etc/nginx/sites-enabled/"
  }

  depends_on = [resource.local_file.nginx_conf]
}

# Restart Nginx after configuration changes
resource "null_resource" "nginx_restart" {
  count = length(var.kasm_instances)

  triggers = {
    subdomain = var.kasm_instances[count.index]["ec2_Subdomain"]
  }

  provisioner "local-exec" {
    command = "sudo systemctl restart nginx"
  }

  depends_on = [null_resource.nginx_symlink]
}

