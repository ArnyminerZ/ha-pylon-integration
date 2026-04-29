"""Number platform for Pylontech Serial."""
from homeassistant.components.number import NumberDeviceClass, RestoreNumber
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entity import PylontechBatteryEntity

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unique_id_prefix = entry.entry_id
    entities = []

    if coordinator.data and coordinator.data.batteries:
        for bat in coordinator.data.batteries:
            bat_id = bat.sys_id
            entities.append(PylontechBatteryCapacityNumber(coordinator, unique_id_prefix, bat_id))

    async_add_entities(entities)


class PylontechBatteryCapacityNumber(PylontechBatteryEntity, RestoreNumber):
    """Representation of a Per-Battery Capacity Number."""

    def __init__(self, coordinator, unique_id_prefix, bat_id):
        super().__init__(coordinator, bat_id)
        
        self._attr_unique_id = f"{unique_id_prefix}_bat{bat_id}_capacity"
        self._attr_translation_key = "battery_capacity"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = NumberDeviceClass.ENERGY_STORAGE
        self._attr_entity_category = EntityCategory.CONFIG
        
        self._attr_native_min_value = 0.5
        self._attr_native_max_value = 10.0
        self._attr_native_step = 0.1
        
        self._attr_native_value = coordinator.default_capacity

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if last_number_data is not None and last_number_data.native_value is not None:
            self._attr_native_value = last_number_data.native_value
        else:
            self._attr_native_value = self.coordinator.default_capacity
        
        self.coordinator.set_battery_capacity(self._bat_id, self._attr_native_value)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.coordinator.set_battery_capacity(self._bat_id, value)
        self.async_write_ha_state()
        
        # Trigger an update to recompute energy stored with new capacity immediately
        await self.coordinator.async_request_refresh()
