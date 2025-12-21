from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PylontechCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pylontech button platform."""
    coordinator: PylontechCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([PylontechSyncTimeButton(coordinator, entry.entry_id)])

class PylontechSyncTimeButton(CoordinatorEntity, ButtonEntity):
    """Button to force sync time to BMS."""

    _attr_has_entity_name = True
    _attr_translation_key = "sync_time"

    def __init__(self, coordinator, unique_id_prefix):
        super().__init__(coordinator)
        self._attr_unique_id = f"{unique_id_prefix}_sync_time"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "system")},
            "name": "Pylontech Stack",
            "manufacturer": "Pylontech",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.async_add_executor_job(self.coordinator.sync_time)
