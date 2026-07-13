from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from typing_extensions import override


class InlineVerticalProgressBar(Widget):
    _1_8: str = "▁"
    _2_8: str = "▂"
    _3_8: str = "▃"
    _4_8: str = "▄"
    _5_8: str = "▅"
    _6_8: str = "▆"
    _7_8: str = "▇"
    _8_8: str = "█"

    DEFAULT_CSS: str = """
    InlineVerticalProgressBar {
        width: 2;
        height: 1;
        margin: 0 1;
    }
    """

    progress: reactive[float] = reactive(0)
    total: reactive[float] = reactive(1)

    def __init__(
        self, progress: float = 0, total: float = 1, id: str | None = None
    ) -> None:
        super().__init__(id=id)
        self.progress = progress
        self.total = total

    @override
    def render(self) -> RenderResult:
        progress = self.progress / self.total
        progress_str = " "
        if progress == 1:
            progress_str = self._8_8
        elif progress >= 7 / 8:
            progress_str = self._7_8
        elif progress >= 6 / 8:
            progress_str = self._6_8
        elif progress >= 5 / 8:
            progress_str = self._5_8
        elif progress >= 4 / 8:
            progress_str = self._4_8
        elif progress >= 3 / 8:
            progress_str = self._3_8
        elif progress >= 2 / 8:
            progress_str = self._2_8
        elif progress >= 1 / 8:
            progress_str = self._1_8
        return progress_str * 2

    def update(self, progress: float) -> None:
        self.progress = progress
