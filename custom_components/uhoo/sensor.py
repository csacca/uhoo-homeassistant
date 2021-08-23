"""UhooSensorEntity class"""

from custom_components.uhoo import UhooDataUpdateCoordinator
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    API_TEMP,
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_LABEL,
    ATTR_UNIQUE_ID,
    ATTR_UNIT,
    DOMAIN,
    NAME,
    SENSOR_TYPES,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors_list = []
    for serial_number in coordinator.data:
        for sensor in SENSOR_TYPES:
            sensors_list.append(UhooSensorEntity(sensor, serial_number, coordinator))

    async_add_entities(sensors_list)


class UhooSensorEntity(CoordinatorEntity, SensorEntity):
    """uHoo Sensor Entity"""

    def __init__(
        self, kind: str, serial_number: str, coordinator: UhooDataUpdateCoordinator
    ):
        super().__init__(coordinator)
        self._kind = kind
        self._serial_number = serial_number

    @property
    def name(self):
        """Return the name of the particular component."""
        return (
            f"uHoo {self._serial_number} {SENSOR_TYPES[self.sensor_type][ATTR_LABEL]}"
        )

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._serial_number}_{SENSOR_TYPES[self.sensor_type][ATTR_UNIQUE_ID]}"

    @property
    def device_info(self):
        # we probably could pull the firmware version if we wanted
        # its in the api somewhere
        return {
            "identifiers": {(DOMAIN, self._serial_number)},
            "name": NAME,
            "model": NAME,
            "manufacturer": NAME,
        }

    @property
    def state(self):
        """State of the sensor."""
        device = self.coordinator.data[self.serial_number]
        state = getattr(device, self.sensor_type)
        if isinstance(state, list):
            state = state[0]
        return state

    @property
    def device_class(self):
        """Return the device class."""
        return SENSOR_TYPES[self.sensor_type][ATTR_DEVICE_CLASS]

    @property
    def icon(self):
        """Return the icon."""
        return SENSOR_TYPES[self.sensor_type][ATTR_ICON]

    @property
    def unit_of_measurement(self):
        """Return unit of measurement."""
        if self.sensor_type == API_TEMP:
            if self.coordinator.user_settings_temp == "f":
                return TEMP_FAHRENHEIT
            else:
                return TEMP_CELSIUS
        else:
            return SENSOR_TYPES[self.sensor_type][ATTR_UNIT]
