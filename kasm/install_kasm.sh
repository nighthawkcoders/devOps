#!/bin/bash

# install_kasm.sh

echo "Hello Terraform!"

# Kasm Single Server Installation
# Reference: https://Kasmweb.com/docs/latest/install/single_server_install.html
cd /tmp
curl -fsSL -o Kasm_release_1.13.1.421524.tar.gz https://Kasm-static-content.s3.amazonaws.com/Kasm_release_1.13.1.421524.tar.gz
tar -xf Kasm_release_1.13.1.421524.tar.gz

# Automate prompts for EULA, Swap Partition, and Port
sudo bash Kasm_release/install.sh --accept-eula --swap-size 8192 -L 8443

# Nginx Installation
sudo apt-get update -y
sudo apt-get install -y nginx

# Certbot Installation
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
