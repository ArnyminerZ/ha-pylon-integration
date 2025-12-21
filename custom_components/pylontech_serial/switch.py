from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PylontechCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pylontech switch platform."""
    coordinator: PylontechCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([PylontechAutoSyncSwitch(coordinator, entry.entry_id)])

class PylontechAutoSyncSwitch(CoordinatorEntity, SwitchEntity, RestoreEntity):
    """Switch to enable auto time sync on boot."""

    _attr_has_entity_name = True
    _attr_translation_key = "auto_sync_time"

    def __init__(self, coordinator, unique_id_prefix):
        super().__init__(coordinator)
        self._attr_unique_id = f"{unique_id_prefix}_auto_sync"
        self._attr_is_on = False # Default off
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "system")},
            "name": "Pylontech Stack",
            "manufacturer": "Pylontech",
        }

    async def async_added_to_hass(self) -> None:
        """Restore last state."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state:
            self._attr_is_on = (last_state.state == "on")
        
        # Apply restoration to coordinator
        self.coordinator.set_auto_sync(self._attr_is_on)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self._attr_is_on = True
        self.coordinator.set_auto_sync(True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        self._attr_is_on = False
        self.coordinator.set_auto_sync(False)
        self.async_write_ha_state()
