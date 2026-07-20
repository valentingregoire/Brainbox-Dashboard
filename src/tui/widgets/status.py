from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Label
from typing_extensions import override

from . import CLR_NOK, CLR_OK, CLR_WARN
from .inline_vertical_progress_bar import InlineVerticalProgressBar


class Status(Horizontal):
    DEFAULT_CSS: str = f"""
    Status {{
        width: auto;
        height: 1;
        margin-right: 2;
    }}
    Status > Label.ok {{
        color: {CLR_OK};
    }}
    Status > Label.warn {{
        color: {CLR_WARN};
    }}
    Status > Label.nok {{
        color: {CLR_NOK};
    }}
    """  # ty:ignore[invalid-attribute-override]

    icon: str = ""
    progress: reactive[int | float | bool] = reactive(0)
    total: reactive[int | float] = reactive(100)
    boolean: bool = False
    show_pb: bool = True

    def __init__(
        self,
        icon: str = "",
        progress: int | float | bool = 0,
        total: int | float = 100,
        boolean: bool = False,
        show_pb: bool = True,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.icon = icon
        self.progress = progress
        self.total = total
        self.boolean = boolean
        self.show_pb = show_pb

    @override
    def compose(self) -> ComposeResult:
        yield Label(self.icon, id="icon")
        if not self.boolean and self.show_pb:
            yield InlineVerticalProgressBar(self.progress, self.total, id="pb")
            yield Label(id="label")

    def update(self, progress: int | float) -> None:
        self.progress = progress
        icon: Label = self.query_one("#icon", Label)
        _ = icon.remove_class("ok")
        _ = icon.remove_class("nok")
        if not self.boolean and self.show_pb:
            label: Label = self.query_one("#label", Label)
            label.update(str(round(progress)))
            self.query_one("#pb", InlineVerticalProgressBar).progress = progress
            pct: float = progress / self.total
            _ = label.remove_class("nok")
            _ = label.remove_class("warn")
            if pct >= 0.75:
                _ = icon.add_class("nok")
                _ = label.add_class("nok")
            elif pct >= 0.5:
                _ = icon.add_class("warn")
                _ = label.add_class("warn")
            else:
                _ = icon.add_class("ok")
                _ = label.add_class("ok")
        else:
            if self.progress:
                _ = icon.add_class("ok")
            else:
                _ = icon.add_class("nok")
