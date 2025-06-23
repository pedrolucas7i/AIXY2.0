#!/bin/bash

# Set permissions for the serial port device
chmod 666 /dev/ttyAML0

# Stop the serial-getty service to free the serial port
systemctl stop serial-getty@ttyAML0.service

logger "startup.sh: Serial port /dev/ttyAML0 permissions set and getty service stopped"