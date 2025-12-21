from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PylontechBattery:
    sys_id: int
    voltage: float
    current: float
    temperature: float
    soc: int
    status: str
    power: float
    raw: str
    # Removed soh/cycles as requested per battery

@dataclass
class PylontechSystem:
    voltage: float
    current: float
    soc: float
    power: float
    energy_in: float
    energy_out: float
    energy_stored: float
    
    # Info Command Data
    cell_count: Optional[int] = None
    spec: Optional[str] = None
    barcode: Optional[str] = None
    fw_version: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    
    # Stat Command Data
    cycles: Optional[int] = None
    soh: Optional[int] = None # System average or from stack stat
    
    raw: str = ""
    
    batteries: List[PylontechBattery] = field(default_factory=list)

    @property
    def battery_count(self) -> int:
        return len(self.batteries)
