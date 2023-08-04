#!/bin/bash

# install_kasm.sh

# Check Cloud-Init Logs: cloud-init-output.log, cloud-init.log
# The logs are located in /var/log/
# Search for echo lines below in an editor to trace failures
echo "Hello Terraform!"

echo "Update packages"
sudo apt-get update -y

# Reference: https://Kasmweb.com/docs/latest/install/single_server_install.html
echo "Kasm Single Server Download"
cd /tmp
curl -fsSL -o Kasm_release_1.13.1.421524.tar.gz https://Kasm-static-content.s3.amazonaws.com/Kasm_release_1.13.1.421524.tar.gz
tar -xf Kasm_release_1.13.1.421524.tar.gz
# Automate prompts for EULA, Swap Partition, and Port
echo "Kasm Single Server Install"
sudo bash Kasm_release/install.sh --accept-eula --swap-size 8192 -L 8443
# 
@echo Nginx Installation
sudo apt-get install -y nginx
#
@echo Certbot Installation
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
