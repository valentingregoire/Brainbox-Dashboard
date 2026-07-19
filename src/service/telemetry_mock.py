from typing_extensions import override

from .telemetry import *

BASE_ADDRESS = "http://127.0.0.1:18181"  # mod desktop


@override
def max_volume() -> int:
    return 207


@override
def volume() -> int:
    return 145


@override
def mod_service_status(service: str) -> int:
    return 2


@override
def snapshot_map() -> dict[str, str]:
    return {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
    }


@override
def snapshot_name() -> str:
    return "three"


@override
def device_status(mac: str) -> bool:
    return True
