# Ventilation for Hospitality
This is part of the Sheffield City Council Ventilation for Hospitality project. This is a data pipeline from Datacake to Research Storage area.

See also the [Vent page on the ITS Wiki](https://itswiki.shef.ac.uk/wiki/Vent).

## Data pipeline

This code is a Python executable module that execute a data pipeline (defined in `vent/workflow.py`) and runs on a regular schedule (defined by `systemd/vent.timer`) and has the following steps:

- Retrieve sensor metadata from Datacake in JSON format
- Download raw data (historical sensor data) from Datacake in JSON format
- Transform (clean) the raw data

The data and metadata are saved to a [Standard Research Storage](https://students.sheffield.ac.uk/it-services/research/storage/standard) area.

The data source is a [GraphQL API](https://docs.datacake.de/api/graphql-api). Queries in the GraphQL language are defined in `vent/templates/*.j2` as [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) templates, which allow for variables to be inserted.

# Installation

This code is designed to be installed on an IT Services [Virtual Server](https://staff.sheffield.ac.uk/it-services/storage/virtual-servers).

Make sure the operating system (OS) packages are up-to-date.

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

# Configuration

The main way to configure the pipeline is to set the environment variables in the file `/home/vent/.env`.

The following options are available:

* `WORKSPACE_ID` is the Datacake workspace identifier (it looks like a UUID)
* `FIELDS` is a JSON array of strings for the names of the fields on Datacake to be downloaded
* `ROOT_DIR` is the directory where data should be saved
* `FREQ` is the time resolution for the clean data. Timestamps will be rounded down to the nearest *x* minutes as determined by this variable.
* `TEMPLATE_DIR` is the directory containing Jinja templates for the queries to run against the GraphQL API.
* The Datacake API access token maybe specified in one of several ways:
  * `DATACAKE_TOKEN` is the access token (keep this secure)
  * `DATACAKE_TOKEN_FILE` is the path of a text file containing the secret (again, keep it secret, keep it safe)
* `LOGLEVEL` determines the verbosity of the messages sent to the standard output and may have one of the Python [logging levels](https://docs.python.org/3/library/logging.html#levels) such as  `WARNING` or  `INFO`.
* `GRAPHQL_URL` is the URL of the web-based GraphQL API.

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

To log in as the server user in a new shell:

```bash
sudo su - vent --shell /bin/bash
```

## Development

Run the pipeline:

```bash
python -m vent --help
```

# Maintenance

The following steps should be performed on a regular schedule to keep the system up-to-date and secure.

* Ensure OS packages are up to date using the [APT package manager](https://help.ubuntu.com/community/AptGet/Howto):
  * `sudo apt update`
  * `sudo apt upgrade`
* Update Python packages:
  * Run security scan using [Safety](https://pypi.org/project/safety/): `/opt/vent/venv/bin/safety check`
  * Install any minor version upgrades: `sudo /opt/vent/venv/bin/pip install --upgrade -r ./requirements.txt`
  * Check for out-of-date Python packages using the [Python Package Installer](https://pip.pypa.io/en/stable/) (PIP) `list` command to find [outdated packages](https://pip.pypa.io/en/stable/user_guide/#listing-packages): `/opt/vent/venv/bin/pip list --outdated`
    * Upgrade these packages (you should test any major version updates in a development environment before installing them on the production environment): `sudo /opt/vent/venv/bin/pip install <package> --upgrade`.
  * Check storage space using `df --human-readable ` and `ncdu`
    * Some ways to clear storage space:
      * Delete old system logs: `sudo journalctl --vacuum-size=500M`
      * Clean up APT caches:
        * `sudo apt autoclean`
        * `sudo apt autoremove`
