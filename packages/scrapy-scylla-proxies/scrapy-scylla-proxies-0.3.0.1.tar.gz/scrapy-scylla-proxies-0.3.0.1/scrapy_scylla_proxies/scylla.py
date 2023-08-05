# For interacting with the Scylla API
import base64
import logging
import random
import re
import threading
import urllib.parse

import requests
from scrapy import signals
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy_scylla_proxies.exceptions import SSPScyllaNotReachableError, SSPScyllaResponseError, SSPScyllaNoProxiesError

SCYLLA_API_PATH = '/api/v1/proxies'
SCYLLA_STATS_PATH = '/api/v1/stats'

VALID_COUNT = 'valid_count'

logger = logging.getLogger('scrapy-scylla-proxies.scylla')


class Scylla(object):
    def __init__(self, uri):
        self.uri = None
        self._check_connection(uri)

    def _check_connection(self, uri):
        """Check if the Scylla API is reachable.

        :param scylla: URL of the Scylla API
        :type scylla: str
        :return: Whether Scylla is reachable
        :rtype: boolean
        """

        logger.debug('Checking connection to Scylla DB.')
        try:
            api = urllib.parse.urljoin(uri, SCYLLA_STATS_PATH)
            # Get the proxy list from scylla
            json_resp = requests.get(api).json()

            # If the valid_count > 0 then we are good to go!
            if int(json_resp[VALID_COUNT]) > 0:
                # Set the Scylla uri
                self.uri = uri
            else:
                raise SSPScyllaNoProxiesError(
                    'No proxies in the Scylla DB, might need to wait a minute.')

        # Catch and raise exceptions
        except requests.exceptions.RequestException:
            raise SSPScyllaNotReachableError('Could not reach the Scylla API.')
        except KeyError:
            raise SSPScyllaResponseError(
                'Expected \'%s\' in response, got %s.' % (VALID_COUNT, json_resp))

    def get_proxies(self, https=True):
        """Get proxy address information from Scylla.

        """

        logger.debug('Fetching proxies.')
        params = {}
        if https:
            params = {'https': 'true'}

        try:
            # Get the proxy list from scylla
            json_resp = requests.get(
                self.uri, params=params).json()
            return json_resp['proxies']
        except requests.exceptions.RequestException:
            raise SSPScyllaNotReachableError('Could not reach the Scylla API.')
