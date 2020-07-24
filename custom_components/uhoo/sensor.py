from homeassistant.const import ATTR_DEVICE_CLASS, TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.helpers.entity import Entity

from . import UhooEntity
from .const import (
    API_TEMP,
    ATTR_ICON,
    ATTR_LABEL,
    ATTR_UNIQUE_ID,
    ATTR_UNIT,
    DATA_COORDINATOR,
    DOMAIN,
    SENSOR_TYPES,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    coordinator = hass.data[DOMAIN][DATA_COORDINATOR][config_entry.entry_id]

    sensors_list = []
    for serial_number in coordinator.data:
        for sensor in SENSOR_TYPES:
            sensors_list.append(UhooSensor(coordinator, serial_number, sensor))

    async_add_entities(sensors_list, False)


class UhooSensor(UhooEntity, Entity):
    """Sensor representing poolsense data."""

    @property
    def name(self):
        """Return the name of the particular component."""
        return f"uHoo {self.serial_number} {SENSOR_TYPES[self.sensor_type][ATTR_LABEL]}"

    @property
    def state(self):
        """State of the sensor."""
        device = self.coordinator.data[self.serial_number]
        state = getattr(device, self.sensor_type)
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

    @property
    def unique_id(self):
        """Return a unique id."""
        return f"{self.serial_number}-{SENSOR_TYPES[self.sensor_type][ATTR_UNIQUE_ID]}"
