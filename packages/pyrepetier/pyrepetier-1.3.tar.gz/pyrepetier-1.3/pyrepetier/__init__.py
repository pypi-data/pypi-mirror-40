from datetime import timedelta
import logging
import os
import requests

logger = logging.getLogger('pyrepetier')

__version__ = '1.3'

SCAN_INTERVAL = timedelta(seconds=5)


class RepetierData():
    """Get the latest sensor data."""

    def __init__(self, parser, config, url, data, api_key):
        """Initialize the data object."""
        self.url = url + ':' + port + '/printer/list/?apikey=' + api_key
        self.data = None
        self.repetier_api_response = parser

    #@Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data."""
        response = requests.get(self.url)
        if response.status_code != 200:
            _LOGGER.warning("Invalid response from API")
        else:
            self.data = self.repetier_api_response(response.json())
