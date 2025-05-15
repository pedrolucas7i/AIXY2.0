#!/bin/bash

echo """
===========================================================
        _      ___  __  __ __   __  ____         ___  
       / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
      / _ \    | |   \  /   \ V /    __) |     | | | |
     / ___ \   | |   /  \    | |    / __/   _  | |_| |
    /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                PROGRAM BY PEDRO LUCAS

===========================================================
"""

# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run this script as root (use sudo)."
  exit 1
fi

# Get the absolute path of the current script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Install or update application
if [ ! -d "/opt/AiXY2.0" ]; then
  echo "[+] Directory /opt/AiXY2.0 not found. Installing files..."
  mkdir -p /opt/AiXY2.0
  cp -r "$SCRIPT_DIR/../." /opt/AiXY2.0/
else
  echo "[✓] /opt/AiXY2.0 already exists. Updating code..."
  cd /opt/AiXY2.0 || {
    echo "❌ Failed to enter /opt/AiXY2.0 directory!"
    exit 1
  }
  git pull
fi

echo """
===========================================================
              STARTING AiXY2.0 PROGRAM
===========================================================
"""

# Switch to normal user (whoever called sudo)
ORIGINAL_USER=$(logname)

# Run the app as the original user with the correct environment
sudo -u "$ORIGINAL_USER" --preserve-env=XDG_RUNTIME_DIR bash -c 'cd /opt/AiXY2.0/src && python3 main.py'
