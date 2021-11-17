"""
Execute data pipeline
"""

import argparse
import logging
import os
import pathlib
import datetime
from getpass import getpass

import vent.workflow

DESCRIPTION = """
Ventilation for hositality data pipelines
"""

DATACAKE_URL = ''


def timestamp(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s)


def load_token(path) -> str:
    try:
        path = pathlib.Path(path)
        with path.open() as file:
            return file.read()
    # No env var specified
    except KeyError:
        return getpass('Enter Datacake API token: ')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-w', '--workspace_id', type=str,
                        help='Datacake workspace identifier',
                        default=os.getenv('WORKSPACE_ID'))
    parser.add_argument('-u', '--url', type=str, help='GraphQL API URL',
                        default=os.getenv('GRAPHQL_URL'))
    parser.add_argument('-f', '--fields', type=str,
                        help='Fields to select (JSON list)',
                        default=os.getenv('FIELDS'))
    parser.add_argument('-t', '--token', type=str,
                        help='Datacake API token')
    parser.add_argument('-s', '--start', type=timestamp,
                        help='Start time ISO 8601 timestamp',
                        default=datetime.datetime.utcnow() - datetime.timedelta(
                            hours=25))
    parser.add_argument('-e', '--end', type=timestamp,
                        help='End time ISO 8601 timestamp',
                        default=datetime.datetime.utcnow())
    parser.add_argument('-f', '--freq', default=os.getenv('FREQ', '2min'))
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    token = args.token or load_token(os.environ['DATACAKE_TOKEN_SECRET_FILE'])

    vent.workflow.run(
        workspace_id=args.workspace_id,
        url=args.url,
        fields=args.fields,
        token=token,
        time_range_start=args.start,
        time_range_end=args.end,
    )


if __name__ == '__main__':
    main()
