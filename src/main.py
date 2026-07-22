from art import text2art
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static
from typing_extensions import override

from service.telemetry import Telemetry
from service.telemetry_mock import TelemetryMock
from tui.screens.sound import SoundScreen
from tui.widgets.inline_button import InlineButton
from tui.widgets.led import LED
from tui.widgets.status import Status
from tui.widgets.volume_control import VolumeChanged, VolumeControl


class BrainboxDashboard(App[None]):
    # CSS_PATH: str = "main.tcss"
    DEFAULT_CSS: str = """  # pyright: ignore[reportIncompatibleVariableOverride]
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
    """  # ty:ignore[invalid-attribute-override]

    telemetry: Telemetry
    snapshot_map: dict[str, str]
    temp: Status = Status(icon="")
    cpu: Status = Status(icon="")
    ram: Status = Status(icon="")
    fan: Status = Status(icon="󰈐", total=0)
    mod_host: Status = Status(icon="󰇅", boolean=True)
    mod_ui: Status = Status(icon="", boolean=True)
    footswitch: Status = Status(icon="󰽒", total=2, show_pb=False)
    tablet: Status = Status(icon="", total=2, show_pb=False)
    laptop: Status = Status(icon="", total=2, show_pb=False)
    # volume: Status = Status(icon="", total=MAX_VOLUME)
    volume: VolumeControl = VolumeControl(0, id="volume_control")
    close_btn: InlineButton = InlineButton("", id="btn_close")
    snapshot: Static = Static(id="snapshot")
    leds: list[LED] = [
        LED(id="led1", classes="status-0"),
        LED(id="led2"),
        LED(id="led3"),
        LED(id="led4"),
    ]

    def __init__(self) -> None:
        super().__init__()
        if self.devtools is not None:
            self.telemetry = TelemetryMock()
        else:
            self.telemetry = Telemetry()
        self.volume.volume = self.telemetry.get_volume()
        self.volume.max = self.telemetry.max_volume
        self.fan.progress = self.telemetry.fan_speed()
        self.fan.total = self.telemetry.max_fan_speed()
        self.snapshot_map = self.telemetry.snapshot_map()

    @override
    def compose(self) -> ComposeResult:
        with Horizontal(id="status-bar"):
            yield self.temp
            yield self.cpu
            yield self.ram
            yield self.fan
            yield self.mod_host
            yield self.mod_ui
            yield self.footswitch
            yield self.tablet
            yield self.laptop
            yield Static(id="spacer")
            with InlineButton(id="btn_volume"):
                yield self.volume
            yield self.close_btn
        yield self.snapshot
        with Horizontal(id="buttons"):
            for led in self.leds:
                yield led

    def on_mount(self) -> None:
        _ = self.set_interval(0.5, self.update_values)

    def update_values(self) -> None:
        cpu_load = self.telemetry.cpu_load()
        self.cpu.update(progress=cpu_load)
        ram_load = self.telemetry.memory_load()
        self.ram.update(progress=ram_load)
        temperature = self.telemetry.cpu_temp()
        self.temp.update(progress=temperature)
        fan_speed = self.telemetry.fan_speed()
        self.fan.update(progress=fan_speed)
        self.mod_host.update(
            self.telemetry.mod_service_status("modep-mod-host")
        )
        self.mod_ui.update(self.telemetry.mod_service_status("modep-mod-ui"))
        status_footswitch: bool = self.telemetry.device_status(
            self.telemetry.MAC_FOOTSWITCH
        )
        status_tablet: bool = self.telemetry.device_status(
            self.telemetry.MAC_TABLET
        )
        status_laptop: bool = self.telemetry.device_status(
            self.telemetry.MAC_LAPTOP
        )
        self.footswitch.update(status_footswitch)
        self.tablet.update(status_tablet)
        self.laptop.update(status_laptop)
        self.volume.volume = self.telemetry.get_volume()
        snapshot_name: str = self.telemetry.snapshot_name()
        self.snapshot.update(str(text2art(snapshot_name, font="big")))
        snapshot_id: int = int(
            self.telemetry.snapshot_id(snapshot_name, self.snapshot_map)
        )
        current_led_id = snapshot_id % len(self.leds)
        for i, led in enumerate(self.leds):
            if i == current_led_id:
                led.update((snapshot_id // len(self.leds)) + 1)
            else:
                led.update(0)

    async def on_inline_button_clicked(
        self, message: InlineButton.Clicked
    ) -> None:  # noqa: F811
        if message.initiator == "btn_close":
            self.exit(message="I quit!")
        elif message.initiator == "btn_volume":
            _ = await self.push_screen(
                SoundScreen(self.telemetry),
                # lambda volume: setattr(self.volume, "volume", volume),
            )

    async def on_volume_changed(self, message: VolumeChanged):
        self.volume.volume = message.new_volume
        _ = self.telemetry.set_volume(message.new_volume)


def run() -> None:
    app = BrainboxDashboard()
    app.run()


if __name__ == "__main__":
    run()
