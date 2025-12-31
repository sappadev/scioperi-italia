"""Config flow for Scioperi Italia."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    DEFAULT_RSS_URL,
    CONF_RSS_URL,
    CONF_REGION_FILTER,
    CONF_SECTOR_FILTER,
    REGIONS,
    SECTORS,
)

_LOGGER = logging.getLogger(__name__)


class ScioperiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Scioperi Italia."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id("scioperi_italia")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title="Scioperi Italia",
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_RSS_URL, 
                    default=DEFAULT_RSS_URL
                ): str,
                vol.Optional(
                    CONF_REGION_FILTER,
                    default="Tutte"
                ): vol.In(REGIONS),
                vol.Optional(
                    CONF_SECTOR_FILTER,
                    default="Tutti"
                ): vol.In(SECTORS),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ScioperiOptionsFlow(config_entry)


class ScioperiOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Scioperi Italia."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_REGION_FILTER,
                        default=self.config_entry.data.get(CONF_REGION_FILTER, "Tutte"),
                    ): vol.In(REGIONS),
                    vol.Optional(
                        CONF_SECTOR_FILTER,
                        default=self.config_entry.data.get(CONF_SECTOR_FILTER, "Tutti"),
                    ): vol.In(SECTORS),
                }
            ),
        )
