import os
import http
import logging

import requests.adapters
import requests.packages.urllib3

USER_AGENT = 'ventilation-for-hospitality'

RETRY_STRATEGY_TOTAL = os.getenv('RETRY_STRATEGY_TOTAL', 3)
RETRY_STRATEGY_BACKOFF_FACTOR = os.getenv('RETRY_STRATEGY_BACKOFF_FACTOR', 1.1)

logger = logging.getLogger(__name__)

RETRY_STRATEGY = dict(
    total=RETRY_STRATEGY_TOTAL,
    status_forcelist=[
        # 400-range
        http.HTTPStatus.TOO_MANY_REQUESTS,
        # 500-range
        http.HTTPStatus.INTERNAL_SERVER_ERROR,
        http.HTTPStatus.BAD_GATEWAY,
        http.HTTPStatus.SERVICE_UNAVAILABLE,
        http.HTTPStatus.GATEWAY_TIMEOUT,
    ],
    backoff_factor=RETRY_STRATEGY_BACKOFF_FACTOR,
)


class GraphQLSession(requests.Session):
    def __init__(self, token, url):
        super().__init__()

        self.headers.update({
            'Authorization': f'Token {token}',
            'User-Agent': os.getenv('USER_AGENT', USER_AGENT),
        })
        self.url = url

    def mount_retry_strategy(self, **kwargs):
        """
        Auto-retry HTTP calls
        https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
        """
        retry_strategy = requests.packages.urllib3.util.retry.Retry(**kwargs)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)

        self.mount('https://', adapter)

        return adapter

    def get(self, query, **kwargs) -> requests.Response:
        logger.debug(query)
        response = super().get(self.url, json=dict(query=query), **kwargs)
        for header, value in response.request.headers.items():
            logger.debug(f'REQUEST HEADER {header}: {value}')
        for header, value in response.headers.items():
            logger.debug(f'RESPONSE HEADER {header}: {value}')
        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.error(response.request.body)
            logger.error(response.text)
            raise
        return response
