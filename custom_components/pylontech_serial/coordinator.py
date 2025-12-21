"""DataUpdateCoordinator for Pylontech Serial."""
import logging
import serial
import time
import threading
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN
from .structs import PylontechSystem
from .parser import PylontechParser

_LOGGER = logging.getLogger(__name__)

class PylontechCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Pylontech battery."""

    def __init__(self, hass: HomeAssistant, port, baud_rate, poll_interval, battery_capacity):
        """Initialize."""
        self.port = port
        self.baud_rate = baud_rate
        self.battery_capacity = battery_capacity
        self.serial = None
        self._lock = threading.Lock()
        
        # Energy calculation state
        self.last_update_time = None
        self.system_energy_in = 0.0
        self.system_energy_out = 0.0
        
        self.auto_sync_time = False # Configurable via switch/options

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=poll_interval),
        )

    def _open_serial(self):
        if self.serial is None:
            _LOGGER.debug(f"Opening serial port {self.port} at {self.baud_rate}")
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=2)
        elif not self.serial.is_open:
             self.serial.open()

    def _close_serial(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.serial = None

    async def _async_update_data(self):
        """Fetch data from the device."""
        # On first run, we might want to read info
        if self.data is None:
             await self.hass.async_add_executor_job(self._read_info_data)
             
             # Check auto-sync on first connection?
             if self.auto_sync_time:
                 await self.hass.async_add_executor_job(self.sync_time)

        return await self.hass.async_add_executor_job(self._read_full_data)

    def _read_info_data(self):
        """Read device info once."""
        with self._lock:
            try:
                self._open_serial()
                self.serial.reset_input_buffer()
                self.serial.write(b"\n")
                time.sleep(0.1)
                self.serial.read_all()

                _LOGGER.debug("Sending 'info' command")
                self.serial.write(b"info\n")
                time.sleep(1.0)
                
                raw_data = self.serial.read_all().decode('ascii', errors='ignore')
                
                # Initialize system if needed, or use a temp one
                # We store persistent data in self.data later, but here we can just parse into a temp object 
                # or attach to self.device_info logic? 
                # Actually, better to store 'info' fields in the main System object.
                # But self.data might be None yet.
                
                # We will create a partial system to hold info logic if we want, 
                # but typically this updates self.device_info or similar for HA entity registry.
                # For now, let's just parse it and store it temporarily or structure it.
                # The Parser expects a System object.
                
                temp_sys = PylontechSystem(0,0,0,0,0,0,0)
                PylontechParser.parse_info(raw_data, temp_sys)
                
                # Store these so we can apply them to the main system object later
                self._cached_info = temp_sys
                
                _LOGGER.info(f"Parsed device info: Model={temp_sys.model}, Ver={temp_sys.fw_version}")

            except Exception as e:
                _LOGGER.warning(f"Failed to fetch device info: {e}")

    def _read_full_data(self):
        """Read data from serial synchronously."""
        with self._lock:
            try:
                self._open_serial()
                
                self.serial.reset_input_buffer()
                self.serial.write(b"\n")
                time.sleep(0.1)
                self.serial.read_all()

                # 1. PWR
                _LOGGER.debug("Sending 'pwr' command")
                self.serial.write(b"pwr\n")
                time.sleep(1.0)
                raw_data_pwr = self.serial.read_all().decode('ascii', errors='ignore')
                
                if "Power Volt" not in raw_data_pwr:
                    # Retry once
                    time.sleep(1.0)
                    raw_data_pwr = self.serial.read_all().decode('ascii', errors='ignore')

                if "Power Volt" not in raw_data_pwr:
                     raise UpdateFailed("Did not receive valid 'pwr' response.")

                # 2. STAT
                _LOGGER.debug("Sending 'stat' command")
                self.serial.write(b"stat\n")
                time.sleep(1.0)
                raw_data_stat = self.serial.read_all().decode('ascii', errors='ignore')

                # Prepare System Object
                # Reuse existing if possible to keep energy counters? 
                # Actually energy counters are stored in self.system_energy_in/out variables in init.
                # So we can create a fresh object and populate it.
                
                # Initialize from cached info if available
                if hasattr(self, '_cached_info'):
                    system = self._cached_info
                    # Reset dynamic values?
                    # The parser overwrites them anyway or assumes defaults.
                    # But better to create strict object.
                    # Lets create new and copy info.
                    info = self._cached_info
                    system = PylontechSystem(
                        voltage=0, current=0, soc=0, power=0, 
                        energy_in=self.system_energy_in, 
                        energy_out=self.system_energy_out, 
                        energy_stored=0,
                        cell_count=info.cell_count,
                        spec=info.spec,
                        barcode=info.barcode,
                        fw_version=info.fw_version,
                        manufacturer=info.manufacturer,
                        model=info.model
                    )
                else:
                    system = PylontechSystem(0,0,0,0, self.system_energy_in, self.system_energy_out, 0)

                # Parse
                PylontechParser.parse_pwr(raw_data_pwr, system)
                PylontechParser.parse_stat(raw_data_stat, system)
                
                # Update Energy Integration
                self._update_energy(system)
                
                # Update Energy Stored
                # Formula: Count * Cap * SOC%
                count = len(system.batteries)
                if count > 0:
                    system.energy_stored = round(count * self.battery_capacity * (system.soc / 100.0), 3)

                return system

            except Exception as e:
                self._close_serial()
                raise UpdateFailed(f"Serial Error: {e}")

    def _update_energy(self, system: PylontechSystem):
        now = datetime.now()
        if self.last_update_time:
            time_diff = (now - self.last_update_time).total_seconds() / 3600.0
            energy_kwh = (system.power * time_diff) / 1000.0
            
            if system.power >= 0:
                self.system_energy_in += abs(energy_kwh)
            else:
                self.system_energy_out += abs(energy_kwh)
        
        self.last_update_time = now
        system.energy_in = round(self.system_energy_in, 3)
        system.energy_out = round(self.system_energy_out, 3)

    def send_raw_command(self, command: str):
        with self._lock:
            try:
                self._open_serial()
                self.serial.reset_input_buffer()
                self.serial.write(b"\n")
                
                cmd_bytes = command.encode("ascii") + b"\n"
                self.serial.write(cmd_bytes)
                time.sleep(0.5)
                return self.serial.read_all().decode('ascii', errors='ignore')
            except Exception as e:
                _LOGGER.error(f"Error sending raw command: {e}")
                raise e

    def sync_time(self):
        """Syncs the BMS time with HA time."""
        cmd = PylontechParser.generate_time_command(datetime.now())
        _LOGGER.info(f"Syncing time with command: {cmd}")
        return self.send_raw_command(cmd)

    def set_auto_sync(self, enabled: bool):
        self.auto_sync_time = enabled
