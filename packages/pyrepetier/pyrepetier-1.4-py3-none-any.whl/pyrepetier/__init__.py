from datetime import timedelta
import logging
import os
import requests

logger = logging.getLogger('pyrepetier')

__version__ = '1.4'

SCAN_INTERVAL = timedelta(seconds=5)


class RepetierData():
    """Get the latest sensor data."""

    def __init__(self, parser, **kwargs):
        """Initialize the data object."""
        url = kwargs.pop('url', None)
        port = kwargs.pop('port', 3344)
        api_key = kwargs.pop('api_key', None)
        self.url = url + ':' + port + '/printer/list/?apikey=' + api_key
        self.data = None
        self.repetier_api_response = parser

    #@Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data."""
        response = requests.get(self.url)
        if response.status_code != 200:
            logger.warning("Invalid response from API")
        else:
            self.data = self.repetier_api_response(response.json())
