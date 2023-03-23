import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from .bin_scraper import get_bin_collection_data

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=12)

async def async_setup_entry(hass, config_entry, async_add_entities):
    urn = config_entry.data["urn"]
    async_add_entities([BinCollectionSensor(urn)], True)

class BinCollectionSensor(Entity):
    def __init__(self, urn):
        self.urn = urn
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Bin Collection"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:trash-can"

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        bin_data = await self.hass.async_add_executor_job(get_bin_collection_data, self.urn)
        this_week = bin_data['this_week']
        future = bin_data['future']

        # Format the data for display in Home Assistant
        this_week_output = []
        for date, bin_days in this_week.items():
            this_week_output.append(date.strftime("%a %d %B %Y"))
            for bin_day in bin_days:
                this_week_output.append(f"{bin_day.name} due {bin_day.date.strftime('%a %d %B %Y')}")

        future_output = []
        for date, bin_days in future.items():
            future_output.append(date.strftime("%a %d %B %Y"))
            for bin_day in bin_days:
                future_output.append(f"{bin_day.name} due {bin_day.date.strftime('%a %d %B %Y')}")

        self._state = '\n'.join(this_week_output + future_output)