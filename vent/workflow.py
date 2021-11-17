"""
Ventilation for Hospitality workflow
"""

import logging
import pathlib
import datetime
from typing import Union

import vent.utils
import vent.http_session

logger = logging.getLogger(__name__)


def serialise(path: Union[str, pathlib.Path], data: str, mode: str = 'w'):
    path = pathlib.Path(path)

    with path.open(mode) as file:
        file.write(data)
        logger.info(f'Wrote "{file.name}"')


def run(workspace_id: str, token: str, fields: str, url: str,
        time_range_start: datetime.datetime,
        time_range_end: datetime.datetime):
    session = vent.http_session.GraphQLSession(token=token, url=url)

    # Download device metadata from Datacake
    device_query = vent.utils.render_template(
        './vent/templates/all_devices.j2', workspace_id=workspace_id)
    devices = session.get(query=device_query).text
    serialise(path='/mnt/data/devices.json', data=devices)

    # Get raw data
    data_query = vent.utils.render_template(
        './vent/templates/device_history.j2', workspace_id=workspace_id,
        fields=fields, time_range_start=time_range_start.isoformat(),
        time_range_end=time_range_end.isoformat())
    raw_data = session.get(query=data_query).text
    serialise(path='/mnt/data/my_data.json', data=raw_data)

    # # Load metadata CSV from research storage
    # deployments = get_deployments()
    #
    # # Transform data
    # clean_data = transform(deployments, raw_data, devices)
    #
    # # Serialise clean data to research storage
    # load_clean_data(clean_data)
