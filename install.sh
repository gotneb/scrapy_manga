#!/bin/bash

echo "Install Mangahub Updater"

cat << EOF > mangahub.service
[Unit]
Description=Mangahub Updater - Update Mangas
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $PWD/main.py
WorkingDirectory=$PWD
Restart=always
User=$USER
TimeoutStopSec=0s

[Install]
WantedBy=multi-user.target
EOF

echo "Coping service file"
sudo cp mangahub.service /etc/systemd/system/

echo "Updating permitions"
sudo chmod 644 /etc/systemd/system/mangahub.service

echo "Loading service"
sudo systemctl daemon-reload

echo "Enabling service"
sudo systemctl enable mangahub.service


echo "The service was created and enabled with sucessfully."
echo ""
echo "To start service: sudo systemctl start mangahub.service"
echo "To restart service: sudo systemctl restart mangahub.service"
echo "To stop service: sudo systemctl stop mangahub.service"

