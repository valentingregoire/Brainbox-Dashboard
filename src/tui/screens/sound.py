from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.css.query import NoMatches
from textual.events import Click
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Static
from textual_slider import Slider
from typing_extensions import override

from service.telemetry import Telemetry
from tui.widgets.inline_button import InlineButton
from tui.widgets.volume_control import VolumeChanged


class SoundScreen(ModalScreen[int]):
    """Little modal screen to adjust the master volume."""

    telemetry: Telemetry
    volume: reactive[int] = reactive(0)
    volume_max: int = 0
    volume_str: reactive[str] = reactive("")

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

        #label {
            width: 100%;
            height: 1;
            text-align: center;
        }
    """

    def __init__(self, telemetry: Telemetry, id: str | None = None) -> None:
        super().__init__(id=id)
        self.telemetry = telemetry
        self.volume = self.telemetry.get_volume()
        self.volume_max = self.telemetry.max_volume

    @override
    def compose(self) -> ComposeResult:
        with Container():
            with Horizontal():
                yield InlineButton("󰝞", id="vol_min")
                yield Slider(
                    0,
                    self.volume_max,
                    value=self.volume,
                    id="slider",
                )
                yield InlineButton("󰝝", id="vol_plus")
            yield Static(self.volume_str, id="label")

    def compute_volume_str(self) -> str:
        """Computes the volume percentage and returns it as a string."""
        if self.volume_max:
            try:
                percent: int = round(self.volume / self.volume_max * 100)
                percent_str = f"{percent}%"
                self.query_one("#label", Static).update(percent_str)
                return percent_str
            except NoMatches:
                return ""
        return ""

    def on_click(self, event: Click) -> None:
        """Handles the click events."""
        if event.widget:
            if event.widget == self:
                _ = self.dismiss(self.volume)
            else:
                slider: Slider = self.query_one("#slider", Slider)
                old_volume: int = self.volume
                if event.widget.id == "vol_min":
                    self.volume -= int(self.volume_max / 20)
                else:
                    self.volume += int(self.volume_max / 20)
                slider.value = self.volume
                _ = event.stop()
                _ = self.post_message(VolumeChanged(self.volume, old_volume))

    def on_slider_changed(self, message: Slider.Changed) -> None:
        """Handles the changes of the slider."""
        old_volume: int = self.volume
        self.volume = message.value
        _ = self.post_message(VolumeChanged(self.volume, old_volume))
