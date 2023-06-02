#!/bin/bash

#update and upgrdae packages
sudo apt update
sudo apt -y upgrade

#install java
sudo apt install openjdk-11-jre-headless

#install docker.io
sudo apt install docker.io

#install pip
sudo apt install python3-pip

#install pulsar python client
pip install pulsar-client

#install MongoDB and dependencies
sudo apt-get install gnupg
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod


pip install pymongo
