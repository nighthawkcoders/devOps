# nginx.tf

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

  depends_on = [
    aws_instance.kasm_server[count.index],
  ]

  triggers = {
    template = data.template_file.nginx_conf_template.rendered
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.nginx_conf_template.rendered}' > /tmp/nginx.conf.tpl"
  }

  provisioner "file" {
    source      = "/tmp/nginx.conf.tpl"
    destination = "/etc/nginx/sites-available/${data.template_file.nginx_conf_template.vars.subdomain}"
  }

  provisioner "remote-exec" {
    inline = [
      "ln -s /etc/nginx/sites-available/${data.template_file.nginx_conf_template.vars.subdomain} /etc/nginx/sites-enabled/"
    ]
  }
}
