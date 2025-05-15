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

# Detect original user and their environment variables
ORIGINAL_USER=$(logname)
USER_ID=$(id -u "$ORIGINAL_USER")
XDG_RUNTIME_DIR="/run/user/$USER_ID"

# Give root permission to access user's PipeWire and PulseAudio sockets
setfacl -m u:root:rwX "$XDG_RUNTIME_DIR/pipewire-0"
setfacl -m u:root:rwX "$XDG_RUNTIME_DIR/pulse/native"

# Run main.py as root but with user’s audio environment
export XDG_RUNTIME_DIR
export PULSE_SERVER="unix:$XDG_RUNTIME_DIR/pulse/native"

cd /opt/AiXY2.0/src || exit 1
python3 main.py
