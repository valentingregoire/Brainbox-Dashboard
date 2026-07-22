from textual.app import RenderResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from typing_extensions import override


class VolumeChanged(Message):
    def __init__(self, new_volume: int, old_volume: int) -> None:
        super().__init__()
        self.new_volume: int = new_volume
        self.old_volume: int = old_volume


class VolumeControl(Widget):
    DEFAULT_CSS: str = """
    VolumeControl {
        width: 3;
        height: 1;
        # margin-right: 3;
        text-align: center;
    }
    """  # ty:ignore[invalid-attribute-override]

    max: int
    volume: reactive[int] = reactive(0)

    def __init__(self, max: int, id: str | None = None) -> None:
        super().__init__(id=id)
        self.volume = 0
        self.max = max

    @override
    def render(self) -> RenderResult:
        volume_percent: int = round(self.volume / self.max * 100)
        if volume_percent == 0:
            return "󰝟 "
        elif volume_percent < 33:
            return "󰕿 "
        elif volume_percent < 66:
            return "󰖀 "
        else:
            return "󰕾 "
