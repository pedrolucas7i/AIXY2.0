#!/bin/bash

echo """
===========================================================
          AIXY2.0 PROJECT DEPENDENCIES INSTALLATION
===========================================================
"""

# Automatically detect non-root user
NON_ROOT_USER=$(logname)

# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (use sudo)."
  exit 1
fi

echo "🔧 Detected user: $NON_ROOT_USER"
echo "📦 Updating packages..."
apt update && apt upgrade -y

echo "📶 Installing Bluetooth and audio packages..."
apt install -y bluetooth bluez pulseaudio pulseaudio-module-bluetooth pavucontrol

echo "🎧 Installing additional audio libraries (PortAudio + VLC)..."
apt install -y libportaudio2 libportaudiocpp0 portaudio19-dev vlc

echo "✅ Enabling and starting Bluetooth service..."
systemctl enable bluetooth
systemctl start bluetooth

echo "🔊 Configuring PulseAudio to support Bluetooth audio..."
mkdir -p /etc/pulse
cat <<EOF > /etc/pulse/system.pa
.include /etc/pulse/default.pa
load-module module-bluetooth-policy
load-module module-bluetooth-discover
EOF

echo "🐍 Installing Python GPIO support..."
apt install -y python3-pip python3-dev gpiod

# Install Python GPIO libraries
pip3 install gpiod --break-system-packages || pip3 install gpiod
pip3 install OPi.GPIO --break-system-packages || pip3 install OPi.GPIO

echo "📄 Installing Python project dependencies from ../src/requirements.txt..."
REQS_PATH="$(dirname "$0")/../src/requirements.txt"
if [ -f "$REQS_PATH" ]; then
    pip3 install -r "$REQS_PATH" --break-system-packages
else
    echo "⚠️  requirements.txt not found at $REQS_PATH!"
fi

echo "👥 Creating gpio group and configuring permissions..."
groupadd -f gpio
usermod -aG gpio "$NON_ROOT_USER"

# Udev rules for GPIO access without root
cat <<EOF > /etc/udev/rules.d/99-gpio.rules
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '\
  chown -R root:gpio /dev/gpiochip* && chmod -R 660 /dev/gpiochip*'"
KERNEL=="gpio*", MODE="0660", GROUP="gpio"
EOF

udevadm control --reload-rules && udevadm trigger

echo "📡 Adding $NON_ROOT_USER to bluetooth group..."
usermod -aG bluetooth "$NON_ROOT_USER"

echo """
===========================================================
            Installation completed successfully!
===========================================================
"""

echo "✅ All setup steps completed!"
echo "🔁 Please reboot or log out and back in to apply all permission changes."
