"""
Ventilation for Hospitality workflow
"""

import logging
import pathlib
import http
import datetime
from typing import Union

import requests.adapters
import requests.packages.urllib3

import vent.utils

logger = logging.getLogger(__name__)

RETRY_STRATEGY = dict(
    total=3,
    status_forcelist=[
        # 400-range
        http.HTTPStatus.TOO_MANY_REQUESTS,
        # 500-range
        http.HTTPStatus.INTERNAL_SERVER_ERROR,
        http.HTTPStatus.BAD_GATEWAY,
        http.HTTPStatus.SERVICE_UNAVAILABLE,
        http.HTTPStatus.GATEWAY_TIMEOUT,
    ],
    backoff_factor=1,
)


def mount_retry_strategy(session: requests.Session, **kwargs):
    """
    Auto-retry HTTP calls
    https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
    """
    retry_strategy = requests.packages.urllib3.util.retry.Retry(
        RETRY_STRATEGY, **kwargs)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)

    for prefix in {'https://', 'https://'}:
        session.mount(prefix, adapter)

    return adapter


def serialise(path: Union[str, pathlib.Path], data: str, mode: str = 'w'):
    path = pathlib.Path(path)

    with path.open(mode) as file:
        file.write(data)
        logger.info(f'Wrote "{file.name}"')


def graphql_get(url: str, token: str, query: str, **kwargs) -> str:
    session = requests.Session()
    mount_retry_strategy(session)
    session.headers.update({'Authorization': f'Token {token}'})
    response = session.get(url, json=dict(query=query), **kwargs)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error(response.request.body)
        logger.error(response.text)
        raise
    return response.text


def run(workspace_id: str, token: str, fields: str, url: str,
        time_range_start: datetime.datetime,
        time_range_end: datetime.datetime):
    # Download device metadata from Datacake
    device_query = vent.utils.render_template(
        './vent/templates/all_devices.j2', workspace_id=workspace_id)
    devices = graphql_get(url=url, query=device_query, token=token)
    serialise(path='/mnt/data/devices.json', data=devices)

    # Get raw data
    data_query = vent.utils.render_template(
        './vent/templates/device_history.j2', workspace_id=workspace_id,
        fields=fields, time_range_start=time_range_start.isoformat(),
        time_range_end=time_range_end.isoformat())
    raw_data = graphql_get(url=url, query=data_query, token=token)
    serialise(path='/mnt/data/my_data.json', data=raw_data)

    # # Load metadata CSV from research storage
    # deployments = get_deployments()
    #
    # # Transform data
    # clean_data = transform(deployments, raw_data, devices)
    #
    # # Serialise clean data to research storage
    # load_clean_data(clean_data)
