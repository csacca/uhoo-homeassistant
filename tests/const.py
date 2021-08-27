"""Constants for uhoo tests."""
from typing import Any, Dict

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

# Mock config data to be used across multiple tests
MOCK_CONFIG = {CONF_USERNAME: "test@example.com", CONF_PASSWORD: "test_password"}

MOCK_DEVICE: Dict[str, Any] = {
    "calibration": 3,
    "createdAt": "2021-01-01T00:00:00.000Z",
    "home": None,
    "latitude": None,
    "longitude": None,
    "macAddress": "684749coffee",
    "name": "Main",
    "serialNumber": "coffeecoffeecoffeecoffee",
    "server": 1,
    "ssid": "TestSSID",
    "status": 1,
}

MOCK_DEVICE_DATA: Dict[str, Any] = {
    "co": {"value": 0},
    "co2": {"value": 1054},
    "datetime": "2021-08-24 22:29:00",
    "dust": {"value": 1},
    "humidity": {"value": 50.7},
    "no2": {"value": 66.7},
    "ozone": {"value": 12.9},
    "pressure": {"value": 1015.7},
    "serialNumber": "coffeecoffeecoffeecoffee",
    "temp": {"value": 74.3},
    "timestamp": 1629858560,
    "voc": {"value": 87},
}
