# Ventilation for Hospitality
Ventilation for Hospitality Project

## Data pipeline

* Get data from Datacake
* Get metadata from Google Drive spreadsheet
* Save data to network stage

# Installation

Make sure the OS packages are up-to-date.

```bash
sudo apt update
sudo apt upgrade
```

Clone the code repository.

Run the installation script as a superuser:

```bash
sudo sh install.sh
```

Install the environment file, which contains options specific to each deployment. There is an example file in this repository called `example.env`. It should have strict file permissions to prevent unauthorised access.

```bash
sudo vi /home/vent/.env
```

Enable the `systemd` timer (this runs the data pipeline on a regular schedule)

```bash
sudo systemctl enable vent.timer
```

[Do not enable](https://askubuntu.com/a/1083647) the service unit `vent.service` because that would mean to start the service at boot time (independent of any timer settings).

To test that it's installed correctly, see the monitoring commands below, and run these commands:

```bash
# Check installed Python version
/opt/vent/venv/bin/python --version

# Check the pipeline is installed
/opt/vent/venv/bin/python -m vent --help
```

# Usage

View the service status:

```bash
sudo systemctl status vent.timer
sudo systemctl status vent.service
```

View the logs:

```bash
sudo journalctl -u vent.service --since "1 hour ago"
```

## Development

Run the pipeline:

```bash
python -m vent
```

# Maintenance

* Ensure 
