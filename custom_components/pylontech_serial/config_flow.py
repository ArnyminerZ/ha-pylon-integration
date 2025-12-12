"""Config flow for Pylontech Serial integration."""
import serial.tools.list_ports
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.usb import UsbServiceInfo
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .const import DOMAIN, CONF_SERIAL_PORT, CONF_BAUD_RATE, CONF_POLL_INTERVAL, CONF_BATTERY_CAPACITY, DEFAULT_BAUD_RATE, DEFAULT_POLL_INTERVAL, DEFAULT_BATTERY_CAPACITY

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pylontech Serial."""

    VERSION = 1


    async def async_step_usb(self, discovery_info: UsbServiceInfo):
        """Handle USB discovery."""
        await self.async_set_unique_id(discovery_info.serial_number or discovery_info.device)
        self._abort_if_unique_id_configured()

        return await self.async_step_user(usb_device=discovery_info.device)

    async def async_step_user(self, user_input=None, usb_device=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Pylontech Battery", data=user_input)

        ports = await self.hass.async_add_executor_job(serial.tools.list_ports.comports)
        list_of_ports = {}
        for port in ports:
            list_of_ports[port.device] = f"{port.device} - {port.description}"

        if usb_device and usb_device not in list_of_ports:
            list_of_ports[usb_device] = usb_device

        default_port = usb_device if usb_device else vol.UNDEFINED

        schema = vol.Schema({
            vol.Required(CONF_SERIAL_PORT, default=default_port): vol.In(list_of_ports),
            vol.Required(CONF_BAUD_RATE, default=DEFAULT_BAUD_RATE): int,
            vol.Required(CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL): int,
            vol.Required(CONF_BATTERY_CAPACITY, default=DEFAULT_BATTERY_CAPACITY): float,
        })

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
