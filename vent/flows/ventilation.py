"""
Ventilation for Hospitality workflow
"""
import pathlib
from typing import Union

import prefect.tasks.secrets
import requests

import vent.utils


@prefect.task
def serialise(path: Union[str, pathlib.Path], data: str, mode: str = 'w'):
    path = pathlib.Path(path)
    logger = prefect.context.get('logger')

    with path.open(mode) as file:
        file.write(data)
        logger.info(f'Wrote "{file.name}"')


@prefect.task
def graphql_get(url: str, token: str, query: str, **kwargs) -> str:
    session = requests.Session()
    session.headers.update({'Authorization': f'Token {token}'})
    response = session.get(url, json=dict(query=query), **kwargs)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger = prefect.context.get('logger')
        logger.error(response.request.body)
        logger.error(response.text)
        raise
    return response.text


# Define workflow
with prefect.Flow('ventilation') as flow:
    # Define parameters
    url = prefect.Parameter('url')
    workspace_id = prefect.Parameter('workspace_id')()
    fields = prefect.Parameter('fields')()
    token = prefect.tasks.secrets.PrefectSecret('DATACAKE_TOKEN')

    # Download device metadata from Datacake
    device_query = vent.utils.render_template(
        './vent/templates/all_devices.j2', workspace_id=workspace_id)
    devices = graphql_get(url=url, query=device_query, token=token)
    serialise(path='/mnt/data/devices.json', data=devices)

    # Get raw data
    data_query = vent.utils.render_template(
        './vent/templates/device_history.j2', fields=fields)
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
