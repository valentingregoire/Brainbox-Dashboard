from typing import Any, Callable

from art import text2art
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Static
from typing_extensions import override

# from service import telemetry
from service import telemetry_mock as telemetry
from tui.screens.sound import SoundScreen
from tui.widgets.inline_button import InlineButton
from tui.widgets.led import LED
from tui.widgets.status import Status
from tui.widgets.volume_control import VolumeControl

MAX_FAN = telemetry.max_fan_speed()
MAX_VOLUME = telemetry.max_volume()
SNAPSHOT_MAP = telemetry.snapshot_map()


class BrainboxDashboard(App[None]):
    # CSS_PATH: str = "main.tcss"
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
    """  # ty:ignore[invalid-attribute-override]

    SCREENS: dict[str, Callable[[], Screen[Any]]] = {"sound": SoundScreen}

    temp: Status = Status(icon="")
    cpu: Status = Status(icon="")
    ram: Status = Status(icon="")
    fan: Status = Status(icon="󰈐", total=MAX_FAN)
    mod_host: Status = Status(icon="󰇅", boolean=True)
    mod_ui: Status = Status(icon="", boolean=True)
    footswitch: Status = Status(icon="󰽒", total=2, show_pb=False)
    tablet: Status = Status(icon="", total=2, show_pb=False)
    laptop: Status = Status(icon="", total=2, show_pb=False)
    # volume: Status = Status(icon="", total=MAX_VOLUME)
    volume: VolumeControl = VolumeControl(MAX_VOLUME)
    close_btn: InlineButton = InlineButton("", id="btn_close")
    snapshot: Static = Static(id="snapshot")
    leds: list[LED] = [
        LED(id="led1", classes="status-0"),
        LED(id="led2"),
        LED(id="led3"),
        LED(id="led4"),
    ]

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
        cpu_load = telemetry.cpu_load()
        self.cpu.update(progress=cpu_load)
        ram_load = telemetry.memory_load()
        self.ram.update(progress=ram_load)
        temperature = telemetry.cpu_temp()
        self.temp.update(progress=temperature)
        fan_speed = telemetry.fan_speed()
        self.fan.update(progress=fan_speed)
        self.mod_host.update(telemetry.mod_service_status("modep-mod-host"))
        self.mod_ui.update(telemetry.mod_service_status("modep-mod-ui"))
        status_footswitch: bool = telemetry.device_status(
            telemetry.MAC_FOOTSWITCH
        )
        status_tablet: bool = telemetry.device_status(telemetry.MAC_TABLET)
        status_laptop: bool = telemetry.device_status(telemetry.MAC_LAPTOP)
        self.footswitch.update(status_footswitch)
        self.tablet.update(status_tablet)
        self.laptop.update(status_laptop)
        self.volume.volume = telemetry.get_volume()
        snapshot_name: str = telemetry.snapshot_name()
        self.snapshot.update(str(text2art(snapshot_name, font="big")))
        snapshot_id: int = int(
            telemetry.snapshot_id(snapshot_name, SNAPSHOT_MAP)
        )
        current_led_id = snapshot_id % len(self.leds)
        for i, led in enumerate(self.leds):
            if i == current_led_id:
                led.update((snapshot_id // len(self.leds)) + 1)
            else:
                led.update(0)

    def on_inline_button_clicked(self, message: InlineButton.Clicked) -> None:  # noqa: F811
        if message.initiator == "btn_close":
            self.exit(message="I quit!")
        elif message.initiator == "btn_volume":
            _ = self.push_screen("sound")

    def on_volume_changed(self, message: VolumeControl.VolumeChanged):
        self.volume.volume = message.value
        _ = telemetry.set_volume(message.value)


def run() -> None:
    app = BrainboxDashboard()
    app.run()


if __name__ == "__main__":
    run()
