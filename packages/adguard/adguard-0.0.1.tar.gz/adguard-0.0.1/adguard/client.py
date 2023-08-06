"""
API Wrapper client for AdGuard Home.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket
import aiohttp
import async_timeout
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
        self._authenticated = False
        self._coonnected = False

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

    async def test_connection(self):
        """Test connection to AdGuard."""
        api = "{}://{}:{}/control/status".format(self.schema, self.host,
                                                 self.port)
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    response = await self.session.get(api)
                else:
                    response = await self.session.get(api, auth=self.auth)
            status = response.status
            if status == 200:
                self._authenticated = True
                self._coonnected = True
                _LOGGER.debug("Sucessfully connected to AdGuard")
            elif status == 401:
                self._coonnected = False
                _LOGGER.error("Authentication error")
            elif status == 404:
                self._authenticated = False
                _LOGGER.error("Endpoint not found error")
            else:
                self._authenticated = False
                self._coonnected = False
                _LOGGER.error("Unexpected error from AdGuard")
        except asyncio.TimeoutError:
            self._coonnected = False
            _LOGGER.error('Timeout error while contacting AdGuard')
        except aiohttp.ClientError as error:
            self._coonnected = False
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except socket.gaierror as error:
            self._coonnected = False
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except Exception as error:  # pylint: disable=W0703
            self._coonnected = False
            _LOGGER.error('Unexpected error from AdGuard, %s', error)

    @property
    async def connection(self):
        """Return connection status."""
        await self.test_connection()
        return {'connected': self._coonnected,
                'authenticated': self._authenticated}
