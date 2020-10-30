from datetime import timedelta
import logging

from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    PRESSURE_HPA,
    TEMP_FAHRENHEIT,
    PERCENTAGE,
)

API_CO = "co"
API_CO2 = "co2"
API_DUST = "dust"
API_HUMIDITY = "humidity"
API_NO2 = "no2"
API_OZONE = "ozone"
API_PRESSURE = "pressure"
API_TEMP = "temp"
API_VOC = "voc"

ATTR_ICON = "icon"
ATTR_LABEL = "label"
ATTR_UNIT = "unit"
ATTR_UNIQUE_ID = "unique_id"

DATA_COORDINATOR = "coordinator"

DOMAIN = "uhoo"

LOGGER = logging.getLogger(__package__)

UPDATE_INTERVAL = timedelta(seconds=60)

SENSOR_TYPES = {
    API_CO: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:molecule-co",
        ATTR_UNIT: CONCENTRATION_PARTS_PER_MILLION,
        ATTR_LABEL: "Carbon monoxide",
        ATTR_UNIQUE_ID: API_CO,
    },
    API_CO2: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:molecule-co2",
        ATTR_UNIT: CONCENTRATION_PARTS_PER_MILLION,
        ATTR_LABEL: "Carbon dioxide",
        ATTR_UNIQUE_ID: API_CO2,
    },
    API_DUST: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:blur",
        ATTR_UNIT: CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ATTR_LABEL: "PM2.5",
        ATTR_UNIQUE_ID: API_DUST,
    },
    API_HUMIDITY: {
        ATTR_DEVICE_CLASS: DEVICE_CLASS_HUMIDITY,
        ATTR_ICON: "mdi:water-percent",
        ATTR_UNIT: PERCENTAGE,
        ATTR_LABEL: "Humidity",
        ATTR_UNIQUE_ID: API_HUMIDITY,
    },
    API_NO2: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:cloud",
        ATTR_UNIT: CONCENTRATION_PARTS_PER_BILLION,
        ATTR_LABEL: "Nitrogen dioxide",
        ATTR_UNIQUE_ID: API_NO2,
    },
    API_OZONE: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:cloud",
        ATTR_UNIT: CONCENTRATION_PARTS_PER_BILLION,
        ATTR_LABEL: "Ozone",
        ATTR_UNIQUE_ID: API_OZONE,
    },
    API_PRESSURE: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:gauge",
        ATTR_UNIT: PRESSURE_HPA,
        ATTR_LABEL: "Air pressure",
        ATTR_UNIQUE_ID: API_PRESSURE,
    },
    API_TEMP: {
        ATTR_DEVICE_CLASS: DEVICE_CLASS_TEMPERATURE,
        ATTR_ICON: "mdi:thermometer",
        ATTR_UNIT: TEMP_FAHRENHEIT,
        ATTR_LABEL: "Temperature",
        ATTR_UNIQUE_ID: API_TEMP,
    },
    API_VOC: {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:cloud",
        ATTR_UNIT: CONCENTRATION_PARTS_PER_BILLION,
        ATTR_LABEL: "Total volatile organic compounds",
        ATTR_UNIQUE_ID: API_VOC,
    },
}
