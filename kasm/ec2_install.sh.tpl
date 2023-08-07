#!/bin/bash

# ec2_install.sh

# Check Cloud-Init Log: cloud-init-output.log
# The log is located in /var/log/
# Search for echo lines below in an editor to trace progres/failures
echo "Hello Terraform!"
#
echo "Update packages"
sudo apt-get update -y
#
# Reference: https://Kasmweb.com/docs/latest/install/single_server_install.html
echo "Kasm Single Server Download"
cd /tmp
curl -fsSL -O https://kasm-static-content.s3.amazonaws.com/kasm_release_1.13.1.421524.tar.gz
tar -xf kasm_release_1.13.1.421524.tar.gz
echo "Kasm Single Server Install"
# Automate prompts for EULA, Swap Partition, Port, Passwords (TBD, remove passords testing passwords)
sudo bash kasm_release/install.sh --accept-eula --swap-size 8192 -L 8443 --admin-password "123Qwerty!" --user-password "123Qwerty!"
tar -xf Kasm_release_1.13.1.421524.tar.gz
# 
echo Nginx Installation
sudo apt-get install -y nginx
#
echo Certbot Installation
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
#
echo Nginx setup
# cat output with Terraform file provisioner updating doman 
# bash -c is critical for heredoc as dollar signs appear in text
sudo bash -c 'cat <<\EOF > "/etc/nginx/sites-available/${SUBDOMAIN}.conf"
server {
    server_name ${DOMAIN};
    listen 80;

    location / {
         # The following configurations must be configured when proxying to Kasm Workspaces

         # WebSocket Support
         proxy_set_header        Upgrade $http_upgrade;
         proxy_set_header        Connection "upgrade";

         # Host and X headers
         proxy_set_header        Host $host;
         proxy_set_header        X-Real-IP $remote_addr;
         proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header        X-Forwarded-Proto $scheme;

         # Connectivity Options
         proxy_http_version      1.1;
         proxy_read_timeout      1800s;
         proxy_send_timeout      1800s;
         proxy_connect_timeout   1800s;
         proxy_buffering         off;

         # Allow large requests to support file uploads to sessions
         client_max_body_size 10M;

         # Proxy to Kasm Workspaces running locally on 8443 using ssl
         proxy_pass https://127.0.0.1:8443 ;
     }
}
EOF'

#
echo Nginx start
sudo ln -s /etc/nginx/sites-available/${SUBDOMAIN}.conf /etc/nginx/sites-enabled/
sudo systemctl start nginx
#
echo Certbot activate
sudo certbot --nginx --noninteractive --agree-tos -m ${EMAIL} -d ${DOMAIN}
#
echo Firewall allow kasm_default_network, kasm_proxy
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw status verbose
#
echo "Bye Terraform!"
