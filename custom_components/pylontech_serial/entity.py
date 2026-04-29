from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

class PylontechSystemEntity(CoordinatorEntity):
    """Base class for Pylontech System entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "system")},
            "name": "Pylontech Stack",
            "manufacturer": "Pylontech",
            "model": "US Series Stack",
        }

class PylontechBatteryEntity(CoordinatorEntity):
    """Base class for Pylontech per-battery entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, bat_id: int):
        super().__init__(coordinator)
        self._bat_id = bat_id
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"battery_{bat_id}")},
            "name": f"Pylontech Module {bat_id}",
            "manufacturer": "Pylontech",
            "model": "US Module",
            "via_device": (DOMAIN, "system"),
        }
