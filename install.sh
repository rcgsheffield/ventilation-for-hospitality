#!/usr/bin/env sh

PYTHON_BINARY=/usr/bin/python3.9
TARGET_DIR=/opt/vent
VENV_DIR=$TARGET_DIR/venv

# Abort on error
set -o nounset
set -o errexit

# Install prerequisite OS packages
apt install -y python3.9 python3.9-pip python3.9-venv

# Update pip package
$PYTHON_BINARY -m pip install pip --upgrade

# Create virtual environment
$PYTHON_BINARY -m pip venv $VENV_DIR
VENV_DIR/bin/pip install -r requirements.txt

# Install data pipeline code
cp -v ./vent $TARGET_DIR/vent

echo "Installing systemd units..."
cp -v ./systemd/vent.service /etc/systemd/system/vent.service
cp -v ./systemd/vent.timer /etc/systemd/system/vent.timer

# Apply changes to systemd units
systemctl daemon-reload
