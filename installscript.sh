#!/bin/bash
#repositories Updates ziehen
sudo apt update
#repositories updaten
sudo apt upgrade -y
#Docker-Installationsskript herunterladen
curl -fsSL https://get.docker.com -o get-docker.sh
#ausführen des Skripts, für die Installation
sudo sh get-docker.sh
apt install docker-compose-plugin -y

sudo usermod -aG docker $USER
