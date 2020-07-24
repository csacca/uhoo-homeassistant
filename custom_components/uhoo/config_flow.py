"""Config flow for Awair."""

from pyuhoo import Client
from pyuhoo.errors import RequestError
import voluptuous as vol

from homeassistant.config_entries import CONN_CLASS_CLOUD_POLL, ConfigFlow
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


class UhooFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for uHoo."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize the config flow."""
        self.data_schema = vol.Schema(
            {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
        )

    async def _show_form(self, errors=None):
        """Show the form to the user."""
        return self.async_show_form(
            step_id="user", data_schema=self.data_schema, errors=errors or {}
        )

    async def async_step_import(self, import_config):
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user(import_config)

    async def async_step_user(self, user_input=None):
        """Handle the start of the config flow."""
        if not user_input:
            return await self._show_form()

        await self.async_set_unique_id(user_input[CONF_USERNAME])
        self._abort_if_unique_id_configured()

        session = async_get_clientsession(self.hass)
        client = Client(
            username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD],
            websession=session,
        )
        try:
            await client.login()
        except RequestError:
            return await self._show_form({"base": "invalid_credentials"})

        return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)
