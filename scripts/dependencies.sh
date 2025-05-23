#!/bin/bash

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


# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (use sudo)."
  exit 1
fi


sudo apt update
sudo apt install libportaudio2 libportaudiocpp0 portaudio19-dev 
sudo apt install git mpg123
sudo apt install -y pulseaudio pulseaudio-module-bluetooth pavucontrol bluez blueman
sudo apt install python3-pip python3-pygame python3-flask
pip3 install pyserial opencv-python sounddevice gtts playsound ollama flask_socketio --break-system-packages


echo """
===========================================================
            Installation completed successfully!
===========================================================
"""

echo "✅ All setup steps completed!"
echo "🔁 Please reboot or log out and back in to apply all permission changes."
