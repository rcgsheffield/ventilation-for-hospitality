"""
Ventilation for Hospitality workflow
"""

import logging
import pathlib
import datetime
import json
import csv
from typing import Union, Iterable

import pandas

import vent.utils
import vent.http_session

logger = logging.getLogger(__name__)

TEMPLATE_DIR = './vent/templates'


def serialise(path: Union[str, pathlib.Path], data: str, mode: str = 'w'):
    path = pathlib.Path(path)

    # Make directory
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    with path.open(mode) as file:
        file.write(data)
        logger.info(f'Wrote "{file.name}"')


def parse_rows(data: str) -> Iterable[dict]:
    """
    Parse GraphQL response into separate data rows
    """
    body = json.loads(data)
    for device in body['data']['allDevices']:
        history = json.loads(device.pop('history'))
        for row in history:
            yield dict(**device, **row)


def write_csv(path: Union[str, pathlib.Path], rows: Iterable[dict]):
    path = pathlib.Path(path)
    writer = None

    with path.open('w') as file:

        for row in rows:
            if not writer:
                writer = csv.DictWriter(file, fieldnames=row.keys())
                writer.writeheader()

            writer.writerow(row)

        logger.info(f'Wrote "{file.name}"')


def run(workspace_id: str, token: str, fields: str, url: str,
        time_range_start: datetime.datetime,
        time_range_end: datetime.datetime, freq='2min', root_dir: str = '.'):
    """
    Execute the workflow
    """

    # Build the target subdirectory to write to
    directory = pathlib.Path(root_dir).joinpath(
        time_range_end.date().isoformat())
    template_dir = pathlib.Path(TEMPLATE_DIR)

    # Connect to Datacake
    with vent.http_session.GraphQLSession(token=token, url=url) as session:
        # Download device metadata from Datacake
        device_query = vent.utils.render_template(
            template_dir.joinpath('all_devices.j2'), workspace_id=workspace_id)
        devices = session.get(query=device_query).text
        serialise(path=directory.joinpath('devices.json'), data=devices)

        # Get raw data
        data_query = vent.utils.render_template(
            template_dir.joinpath('device_history.j2'),
            workspace_id=workspace_id,
            fields=fields,
            time_range_start=time_range_start.isoformat(),
            time_range_end=time_range_end.isoformat()
        )
        raw_data = session.get(query=data_query).text
    serialise(path=directory.joinpath('raw_data.json'), data=raw_data)

    # Transform data
    clean_data = parse_rows(raw_data)
    data = pandas.DataFrame.from_records(clean_data)
    data.info()
    data['time'] = pandas.to_datetime(data['time']).dt.floor(freq)
    print(data.head())
    write_csv(path=directory.joinpath('clean_data.csv'), rows=clean_data)
