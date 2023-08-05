#!/bin/bash

# install_kasm.sh

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
# Automate prompts for EULA, Swap Partition, and Port
sudo bash kasm_release/install.sh --accept-eula --swap-size 8192 -L 8443
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
# Terraform file provisioner
sudo cat <<EOF > "/etc/nginx/sites_available/${SUBDOMAIN}.conf"

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

         # Endpoint of service
         proxy_pass https://localhost:8443;
    }
}
EOF
#
sudo ln -s /etc/nginx/sites_available/${SUBDOMAIN}.conf /etc/nginx/sites_enabled/
echo "Bye Terraform!"

