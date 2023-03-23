import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from bin_scraper import get_bin_collection_data

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ha-stockport-bin-collections'

async def async_setup_entry(hass, config_entry, async_add_entities):
    urn = config_entry.data["urn"]
    async_add_entities([StockportBinCollectionSensor(urn)])

class StockportBinCollectionSensor(Entity):
    def __init__(self, urn):
        self._urn = urn
        self._state = None
        self.update()

    @property
    def name(self):
        return 'Stockport Bin Collections'

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return 'mdi:trash-can-outline'

    def update(self):
        bin_data = get_bin_collection_data(self._urn)
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
