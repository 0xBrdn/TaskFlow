#!/bin/bash

echo "Installation de l'application TaskFlow..."

# Mise à jour du système et installation des dépendances nécessaires
echo "Mise à jour du système et installation des dépendances..."
sudo apt-get update && sudo apt-get install -y \
    x11-xserver-utils \
    docker.io \
    docker-compose

# Ajout de l'utilisateur au groupe Docker
echo "Ajout de l'utilisateur actuel au groupe docker..."
sudo usermod -aG docker $USER

# Configuration de l'affichage pour X11
echo "Configuration de l'affichage pour X11..."
xhost +local:docker

# Préparer l'environnement Docker
echo "Configuration de Docker..."
docker-compose down --remove-orphans
docker-compose build --no-cache

# Obtenir le chemin absolu du projet
PROJECT_DIR="$(pwd)"

# Création du raccourci pour l'application
echo "Création du raccourci pour l'application..."
cat <<EOF | sudo tee /usr/share/applications/TaskFlow.desktop > /dev/null
[Desktop Entry]
Type=Application
Name=TaskFlow
Comment=Gestionnaire de tâches TaskFlow
Exec=gnome-terminal -- bash -c "xhost +local:docker && cd \"${PROJECT_DIR}\" && docker-compose up; bash"
Icon=${PROJECT_DIR}/front_end/authentification/images/authentification/logo.png
Terminal=false
EOF

# Appliquer les permissions nécessaires au raccourci
sudo chmod +x /usr/share/applications/TaskFlow.desktop

# Instructions finales
echo "Installation terminée. Vous pouvez lancer TaskFlow depuis le menu Applications."
echo "Note: Vous devrez vous déconnecter ou redémarrer pour que les changements de groupe Docker prennent effet."
