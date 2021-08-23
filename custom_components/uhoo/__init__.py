"""
Custom integration to integrate uHoo with Home Assistant.

For more details about this integration, please refer to
https://github.com/csacca/uhoo-homeassistant
"""

import asyncio
from typing import Dict, List

from pyuhoo import Client
from pyuhoo.device import Device
from pyuhoo.errors import UnauthorizedError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, PLATFORMS, STARTUP_MESSAGE, UPDATE_INTERVAL


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up uHoo integration from a config entry."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        LOGGER.info(STARTUP_MESSAGE)

    username = config_entry.data.get(CONF_USERNAME)
    password = config_entry.data.get(CONF_PASSWORD)

    session = async_get_clientsession(hass)

    try:
        client = Client(username, password, session)
        await client.login()
    except UnauthorizedError as err:
        LOGGER.error(
            f"Error: received a 401 Unauthorized error attempting to login:\n{err}"
        )

    coordinator = UhooDataUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if config_entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(config_entry, platform)
            )

    config_entry.add_update_listener(async_reload_entry)
    return True


class UhooDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the uHoo API."""

    def __init__(self, hass: HomeAssistant, client: Client) -> None:
        """Initialize."""
        self.client = client
        self.platforms: List[str] = []
        self.user_settings_temp = None

        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def _async_update_data(self) -> Dict[str, Device]:
        try:
            await self.client.get_latest_data()
            self.user_settings_temp = self.client.user_settings_temp
            return self.client.get_devices()
        except Exception as exception:
            LOGGER.error(
                f"Error: an exception occurred while attempting to get latest data:\n{exception}"
            )
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
