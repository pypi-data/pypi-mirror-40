"""General class (For the global/root) endpoints."""
import asyncio
import logging
import socket
import json
from collections import OrderedDict
import aiohttp
import async_timeout
from adguard.common import get_percentage

_LOGGER = logging.getLogger(__name__)


class General(object):
    """A class for the adguard API."""

    def __init__(self, session, loop, api, auth):
        """Initialize the class."""
        self.session = session
        self.loop = loop
        self.api = api
        self.auth = auth
        self._blocked = None
        self._blocked_percentage = None
        self._protection_enabled = None
        self._queries = None
        self._querylog_enabled = None
        self._running = None
        self._stats = None
        self._stats_top = None
        self._status = None
        self._version = None

    async def get_update(self):
        """Get updates."""
        self._stats = await self.get_stats()
        self._stats_top = await self.get_stats_top()
        self._status = await self.get_status()

        self._blocked = self._stats.get('blocked_filtering')
        self._queries = self._stats.get('dns_queries')
        self._blocked_percentage = get_percentage(self._blocked, self._queries)

        self._protection_enabled = self._status.get('protection_enabled')
        self._querylog_enabled = self._status.get('querylog_enabled')

        self._running = self._status.get('running')
        self._version = self._status.get('version')

    async def get_stats(self):
        """Return stats form AdGuard."""
        data = {}
        api = self.api + 'stats'
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    response = await self.session.get(api)
                else:
                    response = await self.session.get(api, auth=self.auth)
            data = await response.json()
        except asyncio.TimeoutError:
            _LOGGER.error('Timeout error while contacting AdGuard')
        except aiohttp.ClientError as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except socket.gaierror as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('Unexpected error from AdGuard, %s', error)
        _LOGGER.debug("AdGuard data: %s", data)
        return data

    async def get_stats_top(self):
        """Return top stats form AdGuard."""
        data = {}
        api = self.api + 'stats_top'
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    response = await self.session.get(api)
                else:
                    response = await self.session.get(api, auth=self.auth)
            data = await response.text()
            data = json.loads(data, object_pairs_hook=OrderedDict)
        except asyncio.TimeoutError:
            _LOGGER.error('Timeout error while contacting AdGuard')
        except aiohttp.ClientError as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except socket.gaierror as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('Unexpected error from AdGuard, %s', error)
        _LOGGER.debug("AdGuard data: %s", data)
        return data

    async def get_status(self):
        """Return status form AdGuard."""
        data = {}
        api = self.api + 'status'
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    response = await self.session.get(api)
                else:
                    response = await self.session.get(api, auth=self.auth)
            data = await response.json()
        except asyncio.TimeoutError:
            _LOGGER.error('Timeout error while contacting AdGuard')
        except aiohttp.ClientError as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except socket.gaierror as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('Unexpected error from AdGuard, %s', error)
        _LOGGER.debug("AdGuard data: %s", data)
        return data

    async def enable_protection(self):
        """Enable protection."""
        api = self.api + 'enable_protection'
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    await self.session.post(api)
                else:
                    await self.session.post(api, auth=self.auth)
            self._protection_enabled = True
        except asyncio.TimeoutError:
            _LOGGER.error('Timeout error while contacting AdGuard')
        except aiohttp.ClientError as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except socket.gaierror as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('Unexpected error from AdGuard, %s', error)

    async def disable_protection(self):
        """Disable protection."""
        api = self.api + 'disable_protection'
        try:
            async with async_timeout.timeout(5, loop=self.loop):
                if self.auth is None:
                    await self.session.post(api)
                else:
                    await self.session.post(api, auth=self.auth)
            self._protection_enabled = False
        except asyncio.TimeoutError:
            _LOGGER.error('Timeout error while contacting AdGuard')
        except aiohttp.ClientError as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except socket.gaierror as error:
            _LOGGER.error('Error connecting to AdGuard, %s', error)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('Unexpected error from AdGuard, %s', error)

    @property
    def blocked(self):
        """Return blocked."""
        return self._blocked

    @property
    def blocked_percentage(self):
        """Return percentage blocked."""
        return self._blocked_percentage

    @property
    def protection_enabled(self):
        """Return bool if protection is enabled."""
        return self._protection_enabled

    @property
    def queries(self):
        """Return DNS queries."""
        return self._queries

    @property
    def querylog_enabled(self):
        """Return bool if querylog is enabled."""
        return self._querylog_enabled

    @property
    def running(self):
        """Return running status."""
        return self._running

    @property
    def stats(self):
        """Return stats."""
        return self._stats

    @property
    def stats_top(self):
        """Return top stats."""
        return self._stats_top

    @property
    def status(self):
        """Return status."""
        return self._status
