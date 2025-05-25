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


sudo apt update -y
sudo apt install -y libportaudio2 libportaudiocpp0 portaudio19-dev 
sudo apt install -y git mpg123
sudo apt install -y pulseaudio pulseaudio-module-bluetooth pavucontrol bluez blueman
sudo apt install -y python3-pip python3-pygame python3-flask
pip3 install pyserial opencv-python sounddevice gtts playsound ollama flask_socketio edge-tts --break-system-packages


echo """
===========================================================
            Installation completed successfully!
===========================================================
"""

echo "✅ All setup steps completed!"
echo "🔁 Please reboot or log out and back in to apply all permission changes."
