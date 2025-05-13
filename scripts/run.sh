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
  echo "Please run this script as root (use sudo)."
  exit 1
fi

git pull

sudo mkdir /opt/AiXY2.0/
sudo cp -r ../* /opt/AiXY2.0/

echo """
===========================================================

                 RUNNING AiXY2.0 PROGRAM

===========================================================
"""
cd /opt/AiXY2.0/src/
sudo python3 /opt/AiXY2.0/src/main.py