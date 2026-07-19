from textual.app import RenderResult
from textual.reactive import reactive
from textual.widgets import Static
from typing_extensions import override

from . import CLR_NOK, CLR_OK, CLR_WARN


class InlineVerticalProgressBar(Static):
    _1_8: str = "▁"
    _2_8: str = "▂"
    _3_8: str = "▃"
    _4_8: str = "▄"
    _5_8: str = "▅"
    _6_8: str = "▆"
    _7_8: str = "▇"
    _8_8: str = "█"

    DEFAULT_CSS: str = f"""
    InlineVerticalProgressBar {{
        width: 2;
        height: 1;
        margin: 0 1;
    }}

    InlineVerticalProgressBar.ok {{
        color: {CLR_OK}
    }}
    InlineVerticalProgressBar.warn {{
        color: {CLR_WARN}
    }}
    InlineVerticalProgressBar.nok {{
        color: {CLR_NOK}
    }}
    """

    progress: reactive[float] = reactive(0)
    total: reactive[float] = reactive(1)
    style: bool = True

    def __init__(
        self,
        progress: float = 0,
        total: float = 1,
        id: str | None = None,
        style: bool = True,
    ) -> None:
        super().__init__(id=id)
        self.progress = progress
        self.total = total
        self.style = style

    @override
    def render(self) -> RenderResult:
        _ = self.remove_class("ok")
        _ = self.remove_class("warn")
        _ = self.remove_class("nok")
        progress = self.progress / self.total
        progress_str = " "
        if progress == 1:
            progress_str = self._8_8
            if self.style:
                _ = self.add_class("nok")
        elif progress >= 7 / 8:
            progress_str = self._7_8
            if self.style:
                _ = self.add_class("nok")
        elif progress >= 6 / 8:
            progress_str = self._6_8
            if self.style:
                _ = self.add_class("nok")
        elif progress >= 5 / 8:
            progress_str = self._5_8
            if self.style:
                _ = self.add_class("warn")
        elif progress >= 4 / 8:
            progress_str = self._4_8
            if self.style:
                _ = self.add_class("warn")
        elif progress >= 3 / 8:
            progress_str = self._3_8
            if self.style:
                _ = self.add_class("ok")
        elif progress >= 2 / 8:
            progress_str = self._2_8
            if self.style:
                _ = self.add_class("ok")
        elif progress >= 1 / 8:
            progress_str = self._1_8
            if self.style:
                _ = self.add_class("ok")
        else:
            if self.style:
                _ = self.add_class("ok")
        return progress_str * 2
