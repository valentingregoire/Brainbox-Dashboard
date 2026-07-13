from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label
from typing_extensions import override

from service import telemetry
from tui.widgets.led import LED
from tui.widgets.status import Status

SNAPSHOT_MAP = telemetry.snapshot_map()
FAN_MAX = telemetry.max_fan_speed()


class BrainboxDashboard(App[None]):
    CSS_PATH: str = "main.tcss"

    cpu: Status = Status(icon="")
    ram: Status = Status(icon="")
    temp: Status = Status(icon="")
    fan: Status = Status(icon="󰈐", total=FAN_MAX)
    snapshot: Label = Label("", id="snapshot")

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self.cpu
            yield self.ram
            yield self.temp
            yield self.fan
        yield self.snapshot
        with Horizontal():
            yield LED(status=0, id="led1")
            yield LED(status=1, id="led2")
            yield LED(status=2, id="led3")
            yield LED(status=2, id="led4")

    def on_mount(self) -> None:
        _ = self.set_interval(0.5, self.update_values)

    def update_values(self) -> None:
        cpu_load = telemetry.cpu_load()
        self.cpu.update(progress=cpu_load)
        ram_load = telemetry.memory_load()
        self.ram.update(progress=ram_load)
        temperature = telemetry.cpu_temp()
        self.temp.update(progress=temperature)
        fan_speed = telemetry.current_fan_speed()
        self.fan.update(progress=fan_speed)
        self.snapshot.update(telemetry.current_snapshot_name())


if __name__ == "__main__":
    app = BrainboxDashboard()
    app.run()
