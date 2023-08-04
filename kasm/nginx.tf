# nginx.tf

resource "null_resource" "nginx_conf" {
  count = length(var.subdomain)

  triggers = {
    template = data.template_file.nginx_conf_template.rendered
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.nginx_conf_template.rendered}' > /tmp/nginx.conf.tpl"
  }

  provisioner "file" {
    source      = "/tmp/nginx.conf.tpl"
    destination = "/etc/nginx/sites-available/${var.subdomain}.conf"
  }

  provisioner "remote-exec" {
    inline = [
      "ln -s /etc/nginx/sites-available/${data.template_file.nginx_conf_template.vars.subdomain} /etc/nginx/sites-enabled/",
      "sudo systemctl start nginx",
      "certbot --nginx --noninteractive --agree-tos -m ${var.email} -d aws_eip.kasm_eip[count.index].name"   
    ]
  }
}
