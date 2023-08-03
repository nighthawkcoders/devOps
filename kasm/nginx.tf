resource "null_resource" "nginx_conf" {
  count = length(var.kasm_ec2)

  depends_on = [
    aws_instance.kasm_server[count.index],
    aws_route53_record.kasm_dns[count.index],
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
      "ln -s /etc/nginx/sites-available/${data.template_file.nginx_conf_template.vars.subdomain} /etc/nginx/sites-enabled/",
      "sudo systemctl start nginx",
      "certbot --nginx --noninteractive --agree-tos -m nighthawkcodingsociety@gmail.com -d ${data.template_file.nginx_conf_template.vars.subdomain}.nighthawkcodingsociety.com"
    ]
  }
}
