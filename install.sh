#!/usr/bin/env sh

PYTHON_VERSION=python3.9
TARGET_DIR=/opt/vent
VENV_DIR=$TARGET_DIR/venv

# Exit immediately if a command exits with a non-zero status
set -e
set -o nounset
set -o errexit

# Install prerequisite OS packages
apt-get update
apt-get -y upgrade
apt-get install -y $PYTHON_VERSION $PYTHON_VERSION-pip $PYTHON_VERSION-venv

# Update pip package
/usr/local/bin/$PYTHON_VERSION -m pip install pip --upgrade

# Create virtual environment
$PYTHON_BINARY -m pip venv $VENV_DIR
VENV_DIR/bin/pip install -r requirements.txt

# Install data pipeline code
cp -v ./vent $TARGET_DIR/vent

echo "Installing systemd units..."
cp -v ./systemd/vent.service /etc/systemd/system/vent.service
cp -v ./systemd/vent.timer /etc/systemd/system/vent.timer

# Apply changes to systemd units

echo "Installing program files..."
mkdir $TARGET_DIR
cp -r ./vent $TARGET_DIR

echo "Installing Python packages..."
$PYTHON_BINARY -m pip install -r $TARGET_DIR/requirements.txt

echo "Installing systemd units..."
cp -v ./systemd/vent.service /etc/systemd/system/
cp -v ./systemd/vent.timer /etc/systemd/system/
systemctl daemon-reload
