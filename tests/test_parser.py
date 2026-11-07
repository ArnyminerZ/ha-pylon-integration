"""Tests for PylontechParser.parse_pwr."""
import importlib.util
import sys
import types
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent / "custom_components" / "pylontech_serial"


def _load(name):
    pkg = sys.modules.setdefault("pylontech_serial", types.ModuleType("pylontech_serial"))
    pkg.__path__ = [str(PKG)]
    spec = importlib.util.spec_from_file_location(f"pylontech_serial.{name}", PKG / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"pylontech_serial.{name}"] = mod
    spec.loader.exec_module(mod)
    return mod


_load("structs")
PylontechParser = _load("parser").PylontechParser

OLD = (
    "Power Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St\n"
    "1     50691  3806   17000  13000  14000  3378   3381   Charge   Normal   Normal   Normal   89%      2025-12-21 20:53:06  Normal   Normal\n"
    "2     50673  4087   16000  13000  14000  3377   3380   Charge   Normal   Normal   Normal   87%      2025-12-21 20:53:04  Normal   Normal\n"
    "3     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -\n"
)

# Newer firmware: four extra *.Id columns before Base.St (synthetic, per issue #9)
NEW = (
    "1     50691  3806   17000  13000  14000  3378   3381   1  2  3  4  Charge   Normal   Normal   Normal   89%      2025-12-21 20:53:06  Normal   Normal\n"
    "2     50673  4087   16000  13000  14000  3377   3380   1  2  3  4  Discharge   Normal   Normal   Normal   87%      2025-12-21 20:53:04  Normal   Normal\n"
)


def test_old_layout():
    s = PylontechParser.parse_pwr(OLD)
    assert [(b.sys_id, b.status, b.soc) for b in s.batteries] == [(1, "Charge", 89), (2, "Charge", 87)]


def test_new_layout():
    s = PylontechParser.parse_pwr(NEW)
    assert [(b.sys_id, b.status, b.soc) for b in s.batteries] == [(1, "Charge", 89), (2, "Discharge", 87)]


def test_missing_percent_skipped():
    line = "1     50691  3806   17000  13000  14000  3378   3381   Charge   Normal   Normal   Normal   x  y  z\n"
    assert PylontechParser.parse_pwr(line).batteries == []
