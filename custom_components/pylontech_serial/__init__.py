"""The Pylontech Serial integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

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

    async def async_send_command(call: ServiceCall) -> dict:
        """Handle the service call."""
        command = call.data.get("command")
        
        # Get the coordinator (assuming one entry for now, or use entry_id if passed)
        # Service is registered globally for the integration, so we need to pick a target or default to the first
        # Ideally services are registered per device, but simple global service is common for single-instance per integration
        # If multiple instances, we might pick the first one from hass.data[DOMAIN]
        
        if not hass.data.get(DOMAIN):
            raise ValueError("No Pylontech integration found")
        
        # Pick the first coordinator
        entry_id = next(iter(hass.data[DOMAIN]))
        coordinator: PylontechCoordinator = hass.data[DOMAIN][entry_id]
        
        response = await hass.async_add_executor_job(coordinator.send_raw_command, command)
        return {"response": response}

    hass.services.async_register(
        DOMAIN, 
        "send_command", 
        async_send_command,
        schema=vol.Schema({vol.Required("command"): cv.string}, extra=vol.ALLOW_EXTRA),
        supports_response=SupportsResponse.OPTIONAL
    )

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
