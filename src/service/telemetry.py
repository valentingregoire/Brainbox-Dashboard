import subprocess
from pathlib import Path

import httpx
import psutil


class Telemetry:
    """A class that can fetch information about the system."""

    BASE_ADDRESS: str = "http://127.0.0.1:8888"  # modep
    HOSTNAME_FOOTSWITCH: str = "esp32c3-0472A8"
    HOSTNAME_TABLET: str = "tablet"
    HOSTNAME_LAPTOP: str = "valentin-laptop"

    def __init__(self) -> None:
        self.max_volume: int = self._max_volume()
        self.snapshot_map: dict[str, str] = self._snapshot_map()

    def cpu_temp(self) -> float:
        """Reads the temperature and returns it as a float with 1 decimal."""
        # return 20.0
        temp = Path("/sys/class/thermal/thermal_zone0/temp").read_text()
        return int(int(temp) / 100) / 10

    def cpu_load(self) -> float:
        """Reads the CPU load percentage and returns it as a float."""
        # return 80.0
        return psutil.cpu_percent(interval=0.2)

    def max_fan_speed(self) -> int:
        """Gets the maximum fan speed state."""
        # return 4
        speed = Path("/sys/class/thermal/cooling_device0/max_state").read_text()
        return int(speed)

    def fan_speed(self) -> int:
        """Gets the current fan speed state."""
        # return 3
        speed = Path("/sys/class/thermal/cooling_device0/cur_state").read_text()
        return int(speed)

    def memory_load(self) -> float:
        """Gets the memory load percentage."""
        # return 22.5
        memory = psutil.virtual_memory()
        return memory.percent

    def _max_volume(self) -> int:
        """Gets the max volume."""
        max = self._cmd(
            "amixer -c 2 cget name='Digital Playback Volume' | grep -oP 'max=\\K[0-9]+' | tail -1"
        )
        return int(max)

    def get_volume(self) -> int:
        """Gets the current volume."""
        volume = self._cmd(
            "amixer -c 2 cget name='Digital Playback Volume' | grep -oP 'values=\\K[0-9]+' | tail -1"
        )
        return int(volume)

    def set_volume(self, volume: int) -> bool:
        result = self._cmd(
            f"amixer -c 2 cset name='Digital Playback Volume' {str(volume)} | grep -oP 'values=\\K[0-9]+' | tail -1"
        )
        return int(result) == volume

    def mod_service_status(self, service: str) -> int:
        """Gets the status of the mod-ui service."""
        status = self._cmd(f"systemctl --user is-active {service}")
        if status == "active":
            return 2
        elif status == "stale":
            return 1
        return 0

    def connected_hosts(self) -> list[str]:
        """Gets the connected devices to the hotspot."""
        devices = self._cmd(
            "cat /var/lib/NetworkManager/dnsmasq-wlan0.leases | awk '{print $4}'"
        ).split("\n")
        return devices

    def _snapshot_map(self) -> dict[str, str]:
        """Gets the snapshot numbers and their corresponding names."""
        response = httpx.get(f"{self.BASE_ADDRESS}/snapshot/list")
        if response.is_success:
            return response.json()
        return {}

    def snapshot_name(self) -> str:
        """Gets the name of the current snapshot."""
        response = httpx.get(f"{self.BASE_ADDRESS}/snapshot/current")
        if response.is_success:
            return response.text
        return "Error"

    def snapshot_id(self, snapshot_name: str) -> str:
        """Gets the id of the current snapshot."""
        return next(
            (k for k, v in self.snapshot_map.items() if v == snapshot_name), "0"
        )

    def _cmd(self, cmd: list[str] | str) -> str:
        """Runs a command and returns the result."""
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return result
