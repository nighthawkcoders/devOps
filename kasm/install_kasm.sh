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
@echo Nginx Installation
sudo apt-get install -y nginx
#
@echo Certbot Installation
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
