#!/usr/bin/env sh

PYTHON_VERSION=python3.9
TARGET_DIR=/opt/vent
VENV_DIR=$TARGET_DIR/venv

# Exit immediately if a command exits with a non-zero status
set -e
set -o nounset
set -o errexit

# Install prerequisite OS packages
apt-get install -y $PYTHON_VERSION $PYTHON_VERSION-venv python3-pip

# Update pip package
$PYTHON_VERSION -m pip install pip --upgrade

# Create virtual environment
$PYTHON_VERSION -m venv $VENV_DIR
$VENV_DIR/bin/pip install -r requirements.txt

# Install data pipeline code
echo "Installing program files..."
cp -r ./vent $TARGET_DIR/vent

useradd --create-home vent

echo "Installing systemd units..."
cp -v ./systemd/vent.service /etc/systemd/system/vent.service
cp -v ./systemd/vent.timer /etc/systemd/system/vent.timer
systemctl daemon-reload
