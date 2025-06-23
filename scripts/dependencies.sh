#!/bin/bash
set -euo pipefail

echo """
===========================================================
        _      ___  __  __ __   __  ____         ___  
       / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
      / _ \    | |   \  /   \ V /    __) |     | | | |
     / ___ \   | |   /  \    | |    / __/   _  | |_| |
    /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

              PROJECT DEPENDENCIES INSTALLATION

===========================================================
"""

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run this script as root (use sudo)."
  exit 1
fi

# Variables
SERVICE_DIR="/home/aixy/service"
SRC_DIR="/home/aixy/src"

# Update and install packages
apt update -y
apt install -y libportaudio2 libportaudiocpp0 portaudio19-dev 
apt install -y git mpg123
apt install -y pulseaudio pulseaudio-module-bluetooth pavucontrol bluez blueman
apt install -y python3-pip python3-pygame python3-flask

# Check for pip3
if ! command -v pip3 &> /dev/null; then
  echo "❌ pip3 not found. Please ensure it is installed."
  exit 1
fi

# Install Python dependencies
pip3 install pyserial opencv-python sounddevice playsound ollama flask_socketio edge-tts --break-system-packages

# Move systemd service files
if [ -f "$SERVICE_DIR/aixy-startup.service" ] && [ -f "$SERVICE_DIR/aixy.service" ]; then
  mv "$SERVICE_DIR/aixy-startup.service" /etc/systemd/system/
  mv "$SERVICE_DIR/aixy.service" /etc/systemd/system/
else
  echo "❌ Service files not found in $SERVICE_DIR"
  exit 1
fi

# Copy startup script and source files
if [ -f "$SERVICE_DIR/aixy-startup.sh" ]; then
  cp "$SERVICE_DIR/aixy-startup.sh" /usr/local/bin/aixy-startup.sh
else
  echo "❌ aixy-startup.sh not found in $SERVICE_DIR"
  exit 1
fi

mkdir -p /usr/local/bin/aixy/
if [ -d "$SRC_DIR" ]; then
  cp -r "$SRC_DIR"/* /usr/local/bin/aixy/
else
  echo "❌ Source directory $SRC_DIR does not exist"
  exit 1
fi

# Enable and reload services
systemctl enable aixy-startup.service
systemctl enable aixy.service
systemctl daemon-reload

# Serial port permissions and service stop
if [ -e /dev/ttyAML0 ]; then
  chmod 666 /dev/ttyAML0
  systemctl stop serial-getty@ttyAML0.service || true
else
  echo "⚠️ /dev/ttyAML0 not found. Skipping serial port config."
fi

echo """
===========================================================
            Installation completed successfully!
===========================================================
"""

echo "✅ All setup steps completed!"
echo "🔁 Please reboot or log out and back in to apply all permission changes."
