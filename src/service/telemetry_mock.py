from typing_extensions import override

from service.telemetry import Telemetry


class TelemetryMock(Telemetry):
    """A mock version of the Telemetry class. Can be used in unit testing, or for development."""

    current_volume: int = 107
    current_snapshot_name: str = "three"

    @override
    def cpu_temp(self) -> float:
        """Reads the temperature and returns it as a float with 1 decimal."""
        return 60.0

    @override
    def cpu_load(self) -> float:
        """Reads the CPU load percentage and returns it as a float."""
        return 80.0

    @override
    def max_fan_speed(self) -> int:
        """Gets the maximum fan speed state."""
        return 4

    @override
    def fan_speed(self) -> int:
        """Gets the current fan speed state."""
        return 3

    @override
    def memory_load(self) -> float:
        """Gets the memory load percentage."""
        return 22.5

    @override
    def _max_volume(self) -> int:
        """Gets the max volume."""
        return 207

    @override
    def get_volume(self) -> int:
        """Gets the current volume."""
        return self.current_volume

    @override
    def set_volume(self, volume: int) -> bool:
        self.current_volume = volume
        return True

    @override
    def mod_service_status(self, service: str) -> int:
        return 2

    @override
    def connected_hosts(self) -> list[Telemetry.DeviceConnection]:
        return [
            self.DeviceConnection(
                self.HOSTNAME_FOOTSWITCH, "192.168.0.2", True, 15
            ),
            self.DeviceConnection(
                self.HOSTNAME_LAPTOP, "192.168.0.3", True, 20
            ),
            self.DeviceConnection(
                self.HOSTNAME_TABLET, "192.168.0.4", True, 25
            ),
            self.DeviceConnection("intruder", "192.168.0.5", True, 30),
        ]

    @override
    def _snapshot_map(self) -> dict[str, str]:
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
    def snapshot_name(self) -> str:
        return self.current_snapshot_name
