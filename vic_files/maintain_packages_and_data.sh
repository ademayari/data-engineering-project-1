#!/bin/bash

# Update all packages
sudo dnf update -y

# Navigate to the specified directory
cd /home/vicuser/data-engineering-project-1/

# Add all changes to git repository
git add .

# Commit changes with a message
git commit -m "data added and checked for package updates"

# Push changes to the remote repository
git push

