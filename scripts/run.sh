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
  # Define log file path
  LOG_FILE="/opt/AiXY2.0/logs/run.log"

  # Ensure the logs directory exists
  mkdir -p /opt/AiXY2.0/logs
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

cd /opt/AiXY2.0/src/ || {
  echo "❌ Error: /opt/AiXY2.0/src/ directory not found!"
  exit 1
}

# Run Python script and log its output
echo "[+] Starting the Python application..."
exec python3 main.py >> "$LOG_FILE" 2>&1
