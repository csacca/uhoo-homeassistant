"""The uHoo Component"""

from asyncio import gather

import async_timeout
from pyuhoo import Client
from pyuhoo.errors import RequestError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DATA_COORDINATOR, DOMAIN, LOGGER, UPDATE_INTERVAL

# from datetime import datetime, timedelta, timezone


PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up uHoo integration."""
    hass.data[DOMAIN] = {DATA_COORDINATOR: {}}

    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up uHoo integration from a config entry."""

    coordinator = UhooDataUpdateCoordinator(hass, config_entry)

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][DATA_COORDINATOR][config_entry.entry_id] = coordinator

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a uHoo config entry."""
    unload_ok = all(
        await gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN][DATA_COORDINATOR].pop(config_entry.entry_id)

    return unload_ok


class UhooEntity(Entity):
    """Implements a common class elements representing the uHoo component."""

    def __init__(self, coordinator, serial_number, sensor_type):
        """Initialize uHoo sensor."""
        self._unique_id = f"{serial_number}-{sensor_type}"
        self.coordinator = coordinator
        self.serial_number = serial_number
        self.sensor_type = sensor_type

    @property
    def unique_id(self):
        """Return a unique id."""
        return self._unique_id

    @property
    def available(self):
        """Return if sensor is available."""
        # device = self.coordinator.data[self.serial_number]
        # is_fresh = (datetime.now(timezone.utc) - device.timestamp) < timedelta(minutes=5)
        # return self.coordinator.last_update_success and is_fresh
        return self.coordinator.last_update_success

    @property
    def should_poll(self) -> bool:
        """Return the polling requirement of the entity."""
        return False

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self) -> None:
        """Request an update of the coordinator for entity."""
        await self.coordinator.async_request_refresh()


class UhooDataUpdateCoordinator(DataUpdateCoordinator):
    """Define an object to hold uHoo data."""

    def __init__(self, hass, config_entry):
        """Initialize."""
        session = async_get_clientsession(hass)
        self.client = Client(
            username=config_entry.data[CONF_USERNAME],
            password=config_entry.data[CONF_PASSWORD],
            websession=session,
        )

        self.hass = hass
        self.entry = config_entry
        self.user_settings_temp = None

        super().__init__(
            hass, LOGGER, name=config_entry.title, update_interval=UPDATE_INTERVAL
        )

    async def login(self):
        await self.client.login()

    async def _async_update_data(self):
        """Get current data from uHoo API"""
        with async_timeout.timeout(10):
            try:
                await self.client.get_latest_data()
                self.user_settings_temp = self.client.user_settings_temp
                return self.client.get_devices()
            except RequestError as err:
                LOGGER.info(
                    f"Failed to retrieve new data from uHoo: {err}\n  Attempting to re-login..."
                )
                try:
                    await self.login()
                    await self.client.get_latest_data()
                    return self.client.get_devices()
                except RequestError as err:
                    raise UpdateFailed(f"Error while retrieving data: {err}")
