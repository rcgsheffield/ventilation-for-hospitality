#!/usr/bin/env sh

PYTHON_VERSION=python3.9
TARGET_DIR=/opt/vent
VENV_DIR=$TARGET_DIR/venv
SERVICE_USER=vent
ENV_VAR_FILE=/home/$SERVICE_USER/.env
DATA_DIR=/mnt/airbods/ventilation

# Exit immediately if a command exits with a non-zero status
set -e
set -o nounset
set -o errexit

# Install prerequisite OS packages
apt-get install -y $PYTHON_VERSION $PYTHON_VERSION-venv python3-pip

# Create virtual environment
$PYTHON_VERSION -m venv $VENV_DIR
# Update pip package
$VENV_DIR/bin/pip install pip --upgrade
$VENV_DIR/bin/pip install -r requirements.txt

# Copy files to a module subdirectory
echo "Installing program files..."
cp -rf ./vent/. $TARGET_DIR/vent/

useradd --create-home $SERVICE_USER || echo "User already exists."

echo "Installing systemd units..."
cp -v ./systemd/vent.service /etc/systemd/system/vent.service
cp -v ./systemd/vent.timer /etc/systemd/system/vent.timer
systemctl daemon-reload

# Install environment variables file for secrets
sudo touch $ENV_VAR_FILE
sudo chown $SERVICE_USER:$SERVICE_USER $ENV_VAR_FILE
sudo chmod 600 $ENV_VAR_FILE

# Create secrets directory
mkdir --parents /home/$SERVICE_USER/.secrets
chown --recursive $SERVICE_USER:$SERVICE_USER /home/$SERVICE_USER/.secrets
chmod 700 /home/$SERVICE_USER/.secrets

# Create data target
mkdir --parents $DATA_DIR
chown --recursive 1000:1000 $DATA_DIR
chmod 775 $DATA_DIR
