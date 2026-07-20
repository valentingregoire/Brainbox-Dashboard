from textual.app import RenderResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from typing_extensions import override


class VolumeControl(Widget):
    class VolumeChanged(Message):
        volume: int = 0

        def __init__(self, volume: int) -> None:
            super().__init__()
            self.value: int = volume

    DEFAULT_CSS: str = """
    VolumeControl {
        width: 3;
        height: 1;
        # margin-right: 3;
        text-align: center;
    }
    """

    max: int
    volume: reactive[int] = reactive(0)

    def __init__(self, max: int, id: str | None = None) -> None:
        super().__init__(id=id)
        self.volume = 0
        self.max = max

    @override
    def render(self) -> RenderResult:
        if self.volume == 0:
            return "󰝟 "
        elif self.volume < 33:
            return "󰕿 "
        elif self.volume < 66:
            return "󰖀 "
        else:
            return "󰕾 "
