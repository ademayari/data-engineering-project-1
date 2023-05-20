#!/bin/bash

# Activate the virtual environment
. /home/vicuser/.local/share/virtualenvs/data-engineering-project-1-ymofnTOH/bin/activate

# Set the environment variables
export SERVICES_DIR=/home/vicuser/data-engineering-project-1/services
export DEPENDENCIES_DIR=/home/vicuser/data-engineering-project-1/dependencies

# Navigate to the project directory
cd /home/vicuser/data-engineering-project-1

# Run the scrape.py script with the TUI argument
python scrape.py -a tui

