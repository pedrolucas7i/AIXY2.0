#!/bin/bash

chmod 777 /dev/ttyAML0

systemctl stop serial-getty@ttyAML0.service

logger "startup.sh: Dispositivo /dev/ttyAML0 liberado e getty parado"