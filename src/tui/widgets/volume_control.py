from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from typing_extensions import override


class VolumeControl(Widget):
    DEFAULT_CSS: str = """
    VolumeControl {
        width: 1;
        height: 1;
        # margin-right: 3;
    }
    """

    max: int
    progress: reactive[int] = reactive(0)

    def __init__(self, max: int, id: str | None = None) -> None:
        super().__init__(id=id)
        self.progress = 55
        self.max = max

    @override
    def render(self) -> RenderResult:
        if self.progress == 0:
            return ""
        elif self.progress < 50:
            return ""
        else:
            return ""
