#!/bin/bash

# Check if the script is run as root or with sudo
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo."
    exit 1
fi

# Update the package repositories
apt update

# Install Docker prerequisites
apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key and repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

# Update repositories again to include Docker repository
apt update

# Install Docker
apt install -y docker-ce docker-ce-cli containerd.io

# Add the current user to the Docker group (optional, allows running Docker without sudo)
usermod -aG docker $USER

# Install Docker Compose
curl -fsSL https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Display Docker and Docker Compose versions
docker --version
docker-compose --version

echo "Docker and Docker Compose installation complete."


#Berechtigungen für Skript setzen
#chmod +x install_docker.sh

#Ausführung als Sudo-user
#sudo ./install_docker.sh

