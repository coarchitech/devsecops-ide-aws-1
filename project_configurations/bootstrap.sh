#!/bin/bash

sudo yum update -y
sudo yum upgrade -y
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform
sudo curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'
sudo unzip awscliv2.zip
sudo ./aws/install
wget https://github.com/gruntwork-io/terragrunt/releases/download/v0.31.0/terragrunt_linux_386 -q
sudo chmod +x terragrunt_linux_386
sudo mv terragrunt_linux_386 /usr/bin/terragrunt
terragrunt --version

#sudo pip install aws-sso-util
#pip install --upgrade pip