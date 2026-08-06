from art import text2art
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.widgets import Static
from typing_extensions import override

from service.telemetry import Telemetry
from service.telemetry_mock import TelemetryMock
from tui.screens.sound import SoundScreen
from tui.widgets.inline_button import InlineButton
from tui.widgets.led import LED
from tui.widgets.separator import Separator
from tui.widgets.status import Status
from tui.widgets.volume_control import VolumeChanged, VolumeControl


class BrainboxDashboard(App[None]):
    DEFAULT_CSS: str = """
        #spacer {
            width: 1fr;
        }

        #snapshot {
            width: 100%;
            align: center middle;
            text-align: center;
            text-style: bold;
        }

        #buttons {
            align: center middle;
        }
    """

    telemetry: Telemetry

    def __init__(self) -> None:
        super().__init__()
        if self.devtools is not None:
            self.telemetry = TelemetryMock()
        else:
            self.telemetry = Telemetry()

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="status-bar"):
            yield Status(icon="", id="temp")
            yield Status(icon="", id="cpu")
            yield Status(icon="", id="ram")
            yield Status(
                icon="󰈐",
                progress=self.telemetry.fan_speed(),
                total=self.telemetry.max_fan_speed(),
                id="fan",
            )
            yield Separator()
            yield Status(icon="󰇅", boolean=True, id="mod_host")
            yield Status(icon="", boolean=True, id="mod_ui")
            yield Separator()
            yield Status(icon="󰽒", total=2, show_pb=False, id="footswitch")
            yield Status(icon=" ", total=2, show_pb=False, id="tablet")
            yield Status(icon=" ", total=2, show_pb=False, id="laptop")
            yield Status(icon="󰭙", total=2, show_pb=False, id="intruder")
            yield Static(id="spacer")
            with InlineButton(id="btn_volume"):
                yield VolumeControl(
                    self.telemetry.get_volume(),
                    self.telemetry.max_volume,
                    id="volume_control",
                )
            yield InlineButton("", id="btn_close")
        yield Static(id="snapshot")
        with Horizontal(id="buttons"):
            yield LED(id="led1", classes="status-0")
            yield LED(id="led2")
            yield LED(id="led3")
            yield LED(id="led4")

    def on_mount(self) -> None:
        _ = self.set_interval(0.5, self.update_values)
        _ = self.set_interval(2, self.update_connections)

    def update_values(self) -> None:
        """Polls the telemetry service and updates the interface accordingly."""
        cpu: Status = self.query_one("#cpu", Status)
        cpu_load: float = self.telemetry.cpu_load()
        cpu.update(progress=cpu_load)
        ram: Status = self.query_one("#ram", Status)
        ram_load: float = self.telemetry.memory_load()
        ram.update(progress=ram_load)
        temp: Status = self.query_one("#temp", Status)
        temperature: float = self.telemetry.cpu_temp()
        temp.update(progress=temperature)
        fan: Status = self.query_one("#fan", Status)
        fan_speed: float = self.telemetry.fan_speed()
        fan.update(progress=fan_speed)
        mod_host: Status = self.query_one("#mod_host", Status)
        mod_host.update(self.telemetry.mod_service_status("modep-mod-host"))
        mod_ui: Status = self.query_one("#mod_ui", Status)
        mod_ui.update(self.telemetry.mod_service_status("modep-mod-ui"))
        volume: VolumeControl = self.query_one("#volume_control", VolumeControl)
        volume.volume = self.telemetry.get_volume()
        snapshot: Static = self.query_one("#snapshot", Static)
        snapshot_name: str = self.telemetry.snapshot_name()
        snapshot.update(str(text2art(snapshot_name, font="big")))
        snapshot_id: int = int(self.telemetry.snapshot_id(snapshot_name))
        leds: list[LED] = [
            self.query_one("#led1", LED),
            self.query_one("#led2", LED),
            self.query_one("#led3", LED),
            self.query_one("#led4", LED),
        ]
        current_led_id = snapshot_id % len(leds)
        for i, led in enumerate(leds):
            if i == current_led_id:
                led.update((snapshot_id // len(leds)) + 1)
            else:
                led.update(0)

    def update_connections(self) -> None:
        """Updates the connected devices status."""
        connected_hosts: list[Telemetry.DeviceConnection] = (
            self.telemetry.connected_hosts()
        )
        footswitch: Status = self.query_one("#footswitch", Status)
        footswitch_status = next(
            ch
            for ch in connected_hosts
            if ch.hostname == self.telemetry.HOSTNAME_FOOTSWITCH
        )
        if footswitch_status:
            footswitch.update(
                footswitch_status.active, str(footswitch_status.ms)
            )
        else:
            footswitch.update(False)
        tablet: Status = self.query_one("#tablet", Status)
        tablet_status = next(
            ch
            for ch in connected_hosts
            if ch.hostname == self.telemetry.HOSTNAME_TABLET
        )
        if tablet_status:
            tablet.update(tablet_status.active, str(tablet_status.ms))
        else:
            tablet.update(False)
        laptop: Status = self.query_one("#laptop", Status)
        laptop_status = next(
            ch
            for ch in connected_hosts
            if ch.hostname == self.telemetry.HOSTNAME_LAPTOP
        )
        if laptop_status:
            laptop.update(laptop_status.active, str(laptop_status.ms))
        else:
            laptop.update(False)
        intruder: Status = self.query_one("#intruder", Status)
        # we negate the result, because True means it's ok, no intruder is found.
        status_intruder: bool = not any(
            ch
            for ch in connected_hosts
            if ch.hostname not in self.telemetry.HOSTNAMES and ch.active
        )
        intruder.update(status_intruder)

    async def on_click(self, message: Click) -> None:
        """Handles the clicks on inline buttons."""
        self.log("click")
        if message.widget:
            self.log(message.widget.id)
            if message.widget.id == "btn_close":
                self.exit(return_code=-1)
            elif message.widget.id in ["btn_volume", "volume_control"]:
                _ = await self.push_screen(
                    SoundScreen(self.telemetry, id="sound_screen"),
                    # lambda volume: setattr(self.volume, "volume", volume),
                )

    async def on_volume_changed(self, message: VolumeChanged):
        """Handles the volume changes from the sound screen, and updates the volume control in the status bar."""
        volume: VolumeControl = self.query_one("#volume_control", VolumeControl)
        volume.volume = message.new_volume
        _ = self.telemetry.set_volume(message.new_volume)


def run() -> None:
    """Run, Forest, run!"""
    app = BrainboxDashboard()
    app.run()


if __name__ == "__main__":
    run()
