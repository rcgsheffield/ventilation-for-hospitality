"""
Ventilation for hospitality workflow
"""

import prefect

import vent.tasks.graphql_task
import vent.resource_managers.http_session

FLOW_KWARGS = dict(
    name='ventilation',
)

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

# Define workflow
with prefect.Flow(**FLOW_KWARGS) as flow:
    # Create HTTP session to datacake
    with vent.resource_managers.http_session.HttpSession() as session:
        # Download device metadata from Datacake
        get_datacake_devices = vent.tasks.graphql_task.GraphqlHttpTask()
        devices = get_datacake_devices(session)

    # Download datacake data
    raw_data = extract_datacake_data()

    # Load metadata CSV from research storage
    deployments = get_deployments()

    # Transform data
    clean_data = transform(deployments, raw_data, devices)

    # Serialise clean data to research storage
    load_clean_data(clean_data)
