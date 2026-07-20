from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Click
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Static
from textual_slider import Slider
from typing_extensions import override

from service import telemetry_mock as telemetry
from tui.widgets.inline_button import InlineButton
from tui.widgets.volume_control import VolumeControl

MAX_VOLUME: int = telemetry.max_volume()
CURRENT_VOLUME: int = telemetry.get_volume()


class SoundScreen(ModalScreen[int]):
    volume: reactive[int] = reactive(CURRENT_VOLUME)
    percent: reactive[int] = reactive(0)
    slider: Slider = Slider(0, MAX_VOLUME, value=CURRENT_VOLUME, id="slider")

    DEFAULT_CSS: str = """
        SoundScreen {
            align: right top;
            # background: $primary 30%;
        }

        SoundScreen > Container {
            width: auto;
            height: auto;
            margin-top: 1;
            align: center middle;
        }

        SoundScreen > Container > Horizontal {
            width: auto;
            height: auto;
        }

        #slider {
            border: none;
            min-height: 1;
            height: 1;
        }

        #percent {
            width: 100%;
            height: 1;
            text-align: center;
        }
    """  # ty:ignore[invalid-attribute-override]

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id=id)
        self.volume = CURRENT_VOLUME
        # self.percent = ""

    @override
    def compose(self) -> ComposeResult:
        with Container():
            with Horizontal():
                yield InlineButton("󰝞", id="vol_min")
                yield self.slider
                yield InlineButton("󰝝", id="vol_plus")
            # with Horizontal():
            yield Static(id="percent")

    def compute_percent(self) -> int:
        percent: int = round(self.volume / self.slider.max * 100)
        self.query_one("#percent", Static).update(f"{percent}%")
        return percent

    def on_inline_button_clicked(self, message: InlineButton.Clicked) -> None:
        if message.initiator == "vol_min":
            # self.slider.value -= 5
            self.volume -= int(self.slider.max / 20)
            self.slider.value = self.volume
            _ = message.stop()
        else:
            # self.slider.value += 5
            self.volume += int(self.slider.max / 20)
            self.slider.value = self.volume
            _ = message.stop()
        _ = self.post_message(VolumeControl.VolumeChanged(self.slider.value))

    def on_click(self, event: Click) -> None:
        if event.widget == self:
            _ = self.dismiss(self.slider.value)

    def on_slider_changed(self, message: Slider.Changed) -> None:
        self.volume = message.value
        _ = self.post_message(VolumeControl.VolumeChanged(message.value))
