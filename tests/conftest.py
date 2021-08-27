"""Global fixtures for uHoo integration."""

from unittest.mock import patch

import pytest
from pyuhoo.device import Device
from pyuhoo.errors import UnauthorizedError

from .const import MOCK_DEVICE, MOCK_DEVICE_DATA

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


@pytest.fixture(name="bypass_async_setup_entry")
def bypass_async_setup_entry_fixture():
    with patch("custom_components.uhoo.async_setup_entry", return_value=True):
        yield


@pytest.fixture(name="mock_device")
def mock_device_fixture() -> Device:
    device = Device(MOCK_DEVICE)
    device.update_data(MOCK_DEVICE_DATA)
    return device


@pytest.fixture(name="bypass_login")
def bypass_login_fixture():
    with patch("custom_components.uhoo.Client.login"):
        yield


@pytest.fixture(name="error_on_login")
def error_login_fixture():
    with patch("custom_components.uhoo.Client.login", side_effect=UnauthorizedError):
        yield


@pytest.fixture(name="bypass_get_latest_data")
def bypass_get_lastest_data_fixture():
    with patch("custom_components.uhoo.Client.get_latest_data"):
        yield


@pytest.fixture(name="bypass_get_devices")
def bypass_get_devices_fixture(mock_device):
    devices = {mock_device.serial_number: mock_device}
    with patch("custom_components.uhoo.Client.get_devices", return_value=devices):
        yield
