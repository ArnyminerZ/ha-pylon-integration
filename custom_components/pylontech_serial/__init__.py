"""The Pylontech Serial integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_SERIAL_PORT, CONF_BAUD_RATE, CONF_POLL_INTERVAL, CONF_BATTERY_CAPACITY
from .coordinator import PylontechCoordinator

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pylontech Serial from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    port = entry.options.get(CONF_SERIAL_PORT, entry.data.get(CONF_SERIAL_PORT))
    baud = entry.options.get(CONF_BAUD_RATE, entry.data.get(CONF_BAUD_RATE))
    interval = entry.options.get(CONF_POLL_INTERVAL, entry.data.get(CONF_POLL_INTERVAL))
    # Battery capacity might be in data (old) or options (new)
    capacity = entry.options.get(CONF_BATTERY_CAPACITY, entry.data.get(CONF_BATTERY_CAPACITY, 2.4))

    coordinator = PylontechCoordinator(hass, port, baud, interval, capacity)

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
