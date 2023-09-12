#!/bin/bash
#repositories Updates ziehen
sudo apt update
#repositories updaten
sudo apt upgrade
#Docker-Installationsskript herunterladen
curl -fsSL https://get.docker.com -o get-docker.sh
#ausführen des Skripts, für die Installation
sudo sh get-docker.sh
apt install docker-compose-plugin

sudo usermod -aG docker $USER


wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1OUZUmXQPcWHZ9sPb6sUdCyiw6mQD18Er' -O todolist.zip
