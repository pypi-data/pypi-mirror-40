"""
API Wrapper client for AdGuard Home.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import logging
import aiohttp
from adguard.const import URL

_LOGGER = logging.getLogger(__name__)


class Client(object):
    """A class for the adguard API."""

    def __init__(self, session, loop, host, port, username, password,
                 ssl=False):
        """Initialize the class."""
        self.schema = 'https' if ssl else 'http'
        self.host = host
        self.port = port
        if username:
            self.auth = aiohttp.BasicAuth(username, password)
        else:
            self.auth = None
        self.loop = loop
        self.session = session

    async def general(self):
        """Return general class object."""
        classurl = URL.format(self.schema, self.host, self.port)
        classobject = None
        try:
            from adguard.general import General
            classobject = General(self.session, self.loop, classurl, self.auth)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('Error connecting to adguard, %s', error)
        return classobject
