from pathlib import Path

import httpx
import psutil

# BASE_ADDRESS: str = "http://127.0.0.1:8888"  # modep
BASE_ADDRESS: str = "http://127.0.0.1:18181"  # mod desktop


def cpu_temp() -> float:
    """Reads the temperature and returns it as a float with 1 decimal."""
    temp = Path("/sys/class/thermal/thermal_zone0/temp").read_text()
    return int(int(temp) / 100) / 10


def cpu_load() -> float:
    """Reads the CPU load percentage and returns it as a float."""
    return psutil.cpu_percent(interval=0.2)


def max_fan_speed() -> int:
    """Gets the maximum fan speed state."""
    speed = 4
    # temp = Path("/sys/class/thermal/thermal_zone0/temp/max_state").read_text()
    return int(speed)


def current_fan_speed() -> int:
    """Gets the current fan speed state."""
    speed = 4
    # speed = Path("/sys/class/thermal/thermal_zone0/cur_state").read_text()
    return int(speed)


def memory_load() -> float:
    """Gets the memory load percentage."""
    memory = psutil.virtual_memory()
    return memory.percent


def snapshot_map() -> dict[str, str]:
    """Gets the snapshot numbers and their corresponding names."""
    response = httpx.get(f"{BASE_ADDRESS}/snapshot/list")
    if response.is_success:
        return response.json()
    return {}


def current_snapshot_name() -> str:
    """Gets the name of the current snapshot."""
    response = httpx.get(f"{BASE_ADDRESS}/snapshot/current")
    if response.is_success:
        return response.text
    return "Unknown"


def current_snapshot_id(snapshot_name: str, snapshot_map: dict[str, str]) -> str | None:
    """Gets the id of the current snapshot."""
    return next((k for k, v in snapshot_map.items() if v == snapshot_name), None)
