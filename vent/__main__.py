"""
Execute data pipeline
"""

import argparse
import json
import logging
import os
import pathlib
import datetime
from getpass import getpass

import vent.workflow

DESCRIPTION = """
Ventilation for hospitality data pipelines
"""

_FIELDS = [
    'TEMPERATURE',
    'HUMIDITY',
    'CO2',
    # 'AIR_QUALITY',
    'LORAWAN_RSSI',
    'LORAWAN_SNR',
    # 'LORAWAN_DATARATE',
]

GRAPHQL_URL = 'https://api.datacake.co/graphql/'
FIELDS = json.dumps(_FIELDS)
DEFAULT_START_TIME = datetime.datetime.utcnow() - datetime.timedelta(hours=25)


def timestamp(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s)


def load_token(path) -> str:
    try:
        path = pathlib.Path(path)
        with path.open() as file:
            return file.read().rstrip('\n')
    # No env var specified
    except (KeyError, TypeError):
        return getpass('Enter Datacake API token: ')


def authenticate(token, url):
    """
    Test user authentication
    """

    from vent.http_session import GraphQLSession

    with GraphQLSession(token=token, url=url) as session:
        query = "{ user { id } }"
        return session.get(query=query).text


def get_args() -> argparse.Namespace:
    """
    Get command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--loglevel', default=os.getenv('LOGLEVEL'))
    parser.add_argument('-w', '--workspace_id', type=str,
                        help='Datacake workspace identifier',
                        default=os.getenv('WORKSPACE_ID'))
    parser.add_argument('-u', '--url', type=str, help='GraphQL API URL',
                        default=os.getenv('GRAPHQL_URL', GRAPHQL_URL))
    parser.add_argument('-f', '--fields', type=str,
                        help='Fields to select (JSON list)',
                        default=os.getenv('FIELDS', FIELDS))
    parser.add_argument('-t', '--token', type=str,
                        help='Datacake API token')
    parser.add_argument('-s', '--start', type=timestamp,
                        help='Start time ISO 8601 timestamp',
                        default=DEFAULT_START_TIME)
    parser.add_argument('-e', '--end', type=timestamp,
                        help='End time ISO 8601 timestamp',
                        default=datetime.datetime.utcnow())
    parser.add_argument('-q', '--freq', default=os.getenv('FREQ', '2min'))
    parser.add_argument('-r', '--root', default=os.getenv('ROOT_DIR', '.'),
                        help='Serialisation directory')
    parser.add_argument('-a', '--auth', help='Check authentication',
                        action='store_true')
    parser.add_argument('--version', action='store_true')

    return parser.parse_args()


def validate_json(data: str):
    json.loads(data)
    return data


def main():
    args = get_args()

    if args.version:
        print(vent.__version__)
        exit()

    # Configure logging
    logging.basicConfig(level=args.loglevel or (
        logging.INFO if args.verbose else args.loglevel))

    # Get API authentication token
    token = args.token or os.getenv('DATACAKE_TOKEN')
    if not token:
        token = load_token(os.getenv('DATACAKE_TOKEN_FILE'))

    if not args.workspace_id:
        raise ValueError('workspace_id is required (or WORKSPACE_ID env var)')

    if args.auth:
        print(authenticate(token=token, url=args.url))
        exit()

    # Execute pipeline
    vent.workflow.run(
        workspace_id=args.workspace_id,
        url=args.url,
        fields=validate_json(args.fields),
        token=token,
        time_range_start=args.start,
        time_range_end=args.end,
        root_dir=args.root,
    )


if __name__ == '__main__':
    main()
