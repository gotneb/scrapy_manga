#!/bin/bash

echo "Stopping mangahub service"
sudo systemctl stop mangahub.service

echo "Disabling mangahub service"
sudo systemctl disable mangahub.service

echo "Removing mangahub service"
sudo rm /etc/systemd/system/mangahub.service

echo "Mangahub Updater Uninstalled with sucessfully."
