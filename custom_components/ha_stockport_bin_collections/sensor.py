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

        # Combine this_week and future bin collections
        all_collections = {**this_week, **future}

        # Get the next bin collection date
        next_date = min(all_collections.keys())

        # Get the bins for the next collection date
        next_bins = all_collections[next_date]

        # Format bin names
        next_bin_names = " & ".join([bin_day.name for bin_day in next_bins])

        # Format the state
        self._state = f"Bins:\n{next_date.strftime('%A %d %B %Y')}: {next_bin_names}"