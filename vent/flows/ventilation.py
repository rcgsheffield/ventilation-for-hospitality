"""
Ventilation for Hospitality workflow
"""

import pathlib

import prefect
import requests

import vent.tasks.graphql_task
import vent.utils


#
# @prefect.task
# def get_datacake_devices():
#     logger = prefect.context.get('logger')
#     logger.debug('get_datacake_devices')
#
#
# @prefect.task
# def extract_datacake_data():
#     logger = prefect.context.get('logger')
#     logger.debug('extract_datacake_data')
#
#
# @prefect.task
# def get_deployments():
#     logger = prefect.context.get('logger')
#     logger.debug('get_deployments')
#
#
# @prefect.task
# def transform(deployments, raw_data, devices):
#     logger = prefect.context.get('logger')
#     logger.debug('transform')
#
#
# @prefect.task
# def load_clean_data(clean_data):
#     logger = prefect.context.get('logger')
#     logger.debug('load_clean_data')
#


@prefect.task
def save_raw_data(raw_data):
    logger = prefect.context.get('logger')

    with pathlib.Path('raw_data.txt').open('w') as file:
        file.write(raw_data)
        logger.info(f'Wrote "{file.name}"')


@prefect.task
def save_devices_raw_data(devices: requests.Response):
    logger = prefect.context.get('logger')

    with pathlib.Path('devices.json').open('w') as file:
        file.write(devices.text)
        logger.info(f'Wrote "{file.name}"')


# Define workflow
with prefect.Flow('ventilation') as flow:
    # Parameters
    workspace_id = prefect.Parameter('workspace_id')
    url = prefect.Parameter('url')
    fields = prefect.Parameter('fields')

    # Create HTTP session to datacake
    with requests.Session() as session:
        # Create GraphQL query
        device_query = vent.utils.render_template(
            './vent/templates/all_devices.j2',
            workspace_id=workspace_id)

        # Download device metadata from Datacake
        get_datacake_devices = vent.tasks.graphql_task.GraphqlHttpTask(
            query=device_query, url=url, session=session)

        # devices_data = get_datacake_devices.run()  # type: requests.Response
        save_devices_raw_data(get_datacake_devices)

        data_query = vent.utils.render_template(
            './vent/templates/device_history.j2', )
    # # Download datacake data
    # raw_data = extract_datacake_data()
    #
    # # Load metadata CSV from research storage
    # deployments = get_deployments()
    #
    # # Transform data
    # clean_data = transform(deployments, raw_data, devices)
    #
    # # Serialise clean data to research storage
    # load_clean_data(clean_data)
