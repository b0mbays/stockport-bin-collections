from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN

DATA_SCHEMA = vol.Schema({vol.Required("urn"): str})


class HaStockportBinCollectionsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            unique_id = user_input["urn"]
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title="Stockport Bin Collection", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("urn"): str}),
            errors=errors,
            description_placeholders={"url": "https://myaccount.stockport.gov.uk/address-finder/bin-collection"},
        )

    @callback
    def async_get_options_flow(config_entry):
        return HaStockportBinCollectionsOptionsFlowHandler(config_entry)


class HaStockportBinCollectionsOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=DATA_SCHEMA)