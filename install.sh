#!/usr/bin/env sh

TARGET_DIR=/opt/vent
VENV_DIR=$TARGET_DIR/venv
PYTHON_BINARY=$VENV_DIR/bin/python3.9

# Exit immediately if a command exits with a non-zero status
set -e

apt-get update
apt-get -y upgrade
apt-get -y install python3.9

echo "Installing program files..."
mkdir $TARGET_DIR
cp -r ./vent $TARGET_DIR

echo "Installing Python packages..."
$PYTHON_BINARY -m pip install -r $TARGET_DIR/requirements.txt

echo "Installing systemd units..."
cp -v ./systemd/vent.service /etc/systemd/system/
cp -v ./systemd/vent.timer /etc/systemd/system/
systemctl daemon-reload
