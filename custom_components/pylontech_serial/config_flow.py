"""Config flow for Pylontech Serial integration."""
import logging
import time

import serialx
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import SerialPortSelector
from homeassistant.helpers.service_info.usb import UsbServiceInfo

from .const import (
    DOMAIN,
    CONF_SERIAL_PORT,
    CONF_BAUD_RATE,
    CONF_POLL_INTERVAL,
    DEFAULT_BAUD_RATE,
    DEFAULT_POLL_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


def _probe_port(port: str, baud_rate: int) -> bool:
    """Open the port and check that the battery answers to `info` (blocking)."""
    ser = serialx.serial_for_url(port, baudrate=baud_rate, read_timeout=2)
    ser.open()
    try:
        ser.reset_read_buffer()
        ser.write(b"\n")
        time.sleep(0.1)
        ser.readall()
        ser.write(b"info\n")
        time.sleep(1.0)
        response = ser.readall().decode("ascii", errors="ignore")
    finally:
        ser.close()
    return bool(response.strip())


async def _async_validate(hass, port: str, baud_rate: int) -> str | None:
    """Return an error key if the port can't be used, otherwise None."""
    try:
        if not await hass.async_add_executor_job(_probe_port, port, baud_rate):
            return "cannot_connect"
    except (OSError, TimeoutError, ValueError, serialx.SerialException):
        # ValueError: malformed URL; OSError: missing/busy device or unreachable host
        return "cannot_connect"
    except Exception:  # noqa: BLE001
        _LOGGER.exception("Unexpected error probing %s", port)
        return "unknown"
    return None


def _schema(port=None, baud=DEFAULT_BAUD_RATE, poll=DEFAULT_POLL_INTERVAL) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_SERIAL_PORT, default=port or vol.UNDEFINED): SerialPortSelector(),
            vol.Required(CONF_BAUD_RATE, default=baud): int,
            vol.Required(CONF_POLL_INTERVAL, default=poll): int,
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pylontech Serial."""

    VERSION = 1

    def __init__(self) -> None:
        self._usb_device: str | None = None

    async def async_step_usb(self, discovery_info: UsbServiceInfo):
        """Handle USB discovery."""
        await self.async_set_unique_id(discovery_info.serial_number or discovery_info.device)
        self._abort_if_unique_id_configured(updates={CONF_SERIAL_PORT: discovery_info.device})
        self._async_abort_entries_match({CONF_SERIAL_PORT: discovery_info.device})

        self._usb_device = discovery_info.device
        self.context["title_placeholders"] = {"name": discovery_info.description or discovery_info.device}
        return await self.async_step_usb_confirm()

    async def async_step_usb_confirm(self, user_input=None):
        """Ask the user to confirm a discovered device before configuring it."""
        if user_input is not None:
            return await self.async_step_user()

        return self.async_show_form(
            step_id="usb_confirm",
            description_placeholders={"device": self._usb_device},
        )

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            port = user_input[CONF_SERIAL_PORT]
            self._async_abort_entries_match({CONF_SERIAL_PORT: port})

            error = await _async_validate(self.hass, port, user_input[CONF_BAUD_RATE])
            if error is None:
                if self.unique_id is None:
                    await self.async_set_unique_id(port)
                    self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Pylontech Battery", data=user_input)
            errors["base"] = error

        suggested = user_input or ({CONF_SERIAL_PORT: self._usb_device} if self._usb_device else {})
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(_schema(), suggested),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}
        entry = self.config_entry

        def current(key, default=None):
            return entry.options.get(key, entry.data.get(key, default))

        if user_input is not None:
            error = await _async_validate(
                self.hass, user_input[CONF_SERIAL_PORT], user_input[CONF_BAUD_RATE]
            )
            if error is None:
                return self.async_create_entry(title="", data=user_input)
            errors["base"] = error

        suggested = user_input or {
            CONF_SERIAL_PORT: current(CONF_SERIAL_PORT),
            CONF_BAUD_RATE: current(CONF_BAUD_RATE, DEFAULT_BAUD_RATE),
            CONF_POLL_INTERVAL: current(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL),
        }
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(_schema(), suggested),
            errors=errors,
        )
