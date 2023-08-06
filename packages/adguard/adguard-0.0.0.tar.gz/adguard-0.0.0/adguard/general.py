"""General class (For the global/root) endpoints."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

from adguard.const import HEADERS

_LOGGER = logging.getLogger(__name__)


class General(object):
    """A class for the adguard API."""

    def __init__(self, session, loop, api, auth):
        """Initialize the class."""
        self.session = session
        self.loop = loop
        self.api = api
        self.auth = auth

    async def get_stats(self):
        """Return stats form AdGuard."""
        data = {}
        api = self.api + 'stats'
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    response = await self.session.get(api, headers=HEADERS)
                else:
                    response = await self.session.get(api, auth=self.auth,
                                                      headers=HEADERS)
            data = await response.json()
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching data from AdGuard, %s', error)
        _LOGGER.debug("AdGuard data: %s", data)
        return data
