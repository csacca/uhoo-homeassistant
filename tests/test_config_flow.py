"""Test uHoo config flow process."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.uhoo.const import DOMAIN
from homeassistant import data_entry_flow
from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import MOCK_CONFIG


async def test_show_form(hass):
    """Test that the form is served with no input."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == SOURCE_USER


async def test_invalid_credentials(hass, error_on_login):
    """Test that errors are shown when credentials are invalid."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=MOCK_CONFIG
    )

    assert result["errors"] == {"base": "auth"}


async def test_second_instance_error(
    hass, bypass_login, bypass_get_latest_data, bypass_get_devices
):
    """Test that errors are shown when a second instance is added."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="1",
        data=MOCK_CONFIG,
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=MOCK_CONFIG
    )

    assert result["type"] == "abort"
    assert result["reason"] == "single_instance_allowed"


async def test_create_entry(
    hass,
    bypass_async_setup_entry,
    bypass_login,
    bypass_get_latest_data,
    bypass_get_devices,
):
    """Test that the user step works."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=MOCK_CONFIG
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["data"][CONF_USERNAME] == MOCK_CONFIG[CONF_USERNAME]
    assert result["data"][CONF_PASSWORD] == MOCK_CONFIG[CONF_PASSWORD]
