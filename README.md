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

Install any secrets into the environment file, which should have strict file permissions.

```bash
sudo vi /home/vent/.env
```

Enable the `systemd` timer (this runs the data pipeline on a regular schedule)

```bash
sudo systemctl enable vent.timer
```

# Usage

View the service status:

```bash
sudo systemctl status vent.timer
sudo systemctl status vent.service
```

Enable the service:

```bash
sudo systemctl enable vent.timer
```



## Development

Run the pipeline:

```bash
python -m vent
```

# Maintenance

* Ensure 
