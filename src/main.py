from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, ProgressBar
from typing_extensions import override

from service import telemetry

SNAPSHOT_MAP = telemetry.snapshot_map()
FAN_MAX = telemetry.max_fan_speed()


class BrainboxDashboard(App[None]):
    CSS_PATH: str = "main.tcss"

    cpu_pb: ProgressBar = ProgressBar(total=100, show_eta=False)
    ram_pb: ProgressBar = ProgressBar(total=100, show_eta=False)
    temp_pb: ProgressBar = ProgressBar(total=100, show_eta=False)
    fan_pb: ProgressBar = ProgressBar(total=FAN_MAX, show_eta=False)
    snapshot: Label = Label("", id="snapshot")

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="status-bar"):
            yield Label("")
            yield self.cpu_pb
            yield Label("")
            yield self.ram_pb
            yield Label("")
            yield self.temp_pb
            yield Label("󰈐")
            yield self.fan_pb
        yield self.snapshot

    def on_mount(self) -> None:
        _ = self.set_interval(0.5, self.update_values)

    def update_values(self) -> None:
        cpu_load = telemetry.cpu_load()
        self.cpu_pb.update(progress=cpu_load)
        ram_load = telemetry.memory_load()
        self.ram_pb.update(progress=ram_load)
        temp_percentage = telemetry.cpu_temp()
        self.temp_pb.update(progress=temp_percentage)
        fan_speed = telemetry.current_fan_speed()
        self.fan_pb.update(progress=fan_speed)
        self.snapshot.update(telemetry.current_snapshot_name())


if __name__ == "__main__":
    app = BrainboxDashboard()
    app.run()
