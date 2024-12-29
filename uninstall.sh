#!/bin/bash

# Script to uninstall TaskFlow-specific Docker containers and resources

echo "Stopping and removing TaskFlow Docker containers and images..."

# Stop and remove containers
docker-compose down

# Remove TaskFlow-specific images
docker rmi sae502-taskflow-test-docker-taskflow-app

# Remove TaskFlow-specific volumes
docker volume prune -f

# Remove Docker network specific to TaskFlow
docker network prune -f

echo "Removing application shortcut..."
# Remove application shortcut
rm -f /usr/share/applications/TaskFlow.desktop

echo "Uninstallation complete. TaskFlow and related Docker containers have been removed."
