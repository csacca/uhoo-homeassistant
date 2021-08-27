"""Test uHoo setup process."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.uhoo import UhooDataUpdateCoordinator, async_setup_entry
from custom_components.uhoo.const import DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.setup import async_setup_component

from .const import MOCK_CONFIG


async def test_setup_no_config(hass):
    """Test DOMAIN is empty if there is no config."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    assert DOMAIN not in hass.config_entries.async_domains()


async def test_async_setup_entry(
    hass, bypass_login, bypass_get_latest_data, bypass_get_devices
):
    """Test a successful setup entry."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="1",
        data=MOCK_CONFIG,
    )
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert type(hass.data[DOMAIN][config_entry.entry_id]) == UhooDataUpdateCoordinator


async def test_async_setup_entry_exception(hass, error_on_login):
    """Test when API raises an exception during entry setup."""

    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG)

    assert await async_setup_entry(hass, config_entry) is False


async def test_unload_entry(
    hass, bypass_login, bypass_get_latest_data, bypass_get_devices
):
    """Test successful unload of entry."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="1",
        data=MOCK_CONFIG,
    )
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)
