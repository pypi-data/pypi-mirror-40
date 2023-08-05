"""
Get information from the BrewDog API (PunkAPI).

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout
from brewdog.const import (BASE_URL, HEADERS)

_LOGGER = logging.getLogger(__name__)


class API(object):
    """A class for the BrewDog API."""

    def __init__(self, loop, session):
        """Initialize the class."""
        self._loop = loop
        self._session = session

    async def get_beer_random(self):
        """Get information about a random beer."""
        url = BASE_URL + '/random'
        returnvalue = []
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url, headers=HEADERS)
                returnvalue = await response.json()
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Brewdog, %s', error)
        return returnvalue

    async def get_beer_single(self, beer_id):
        """Get information about a single beer by ID."""
        url = BASE_URL + '/' + beer_id
        returnvalue = []
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(url, headers=HEADERS)
                returnvalue = await response.json()
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Brewdog, %s', error)
        return returnvalue
