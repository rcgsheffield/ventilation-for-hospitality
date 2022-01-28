#!/bin/bash

# Historic data back-fill script
# Usage:
# sudo -u vent bash historic.sh

# Abort on error
set -e

# Configure environment
set -a # automatically export all variables
source /home/vent/.env
set +a
export PYTHONPATH=/opt/vent

# Iterate over historic dates
# Start date
day="2021-11-01"
# Loop until current date
while [ "$day" != $(date -I) ]; do
  echo $day

  # Run pipeline for this day
  /opt/vent/venv/bin/python -m vent --start $day

  # Add one day
  day=$(date -I -d "$day + 1 day")

done
