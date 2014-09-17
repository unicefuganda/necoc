#!/bin/bash

sudo echo "[mongodb]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/
gpgcheck=0
enabled=1" > /etc/yum.repos.d/mongodb.repo

sudo yum update -y
sudo yum install -y mongodb-org

pip install -r requirements.txt
