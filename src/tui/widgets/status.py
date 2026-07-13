from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Label
from typing_extensions import override

from tui.widgets.inline_vertical_progress_bar import InlineVerticalProgressBar


class Status(Horizontal):
    DEFAULT_CSS: str = """
    Status {
        width: auto;
        height: 1;
        margin-right: 2;
    }
    """

    progress: reactive[int | float] = reactive(0)
    total: reactive[int | float] = reactive(100)
    icon: str = ""

    def __init__(
        self,
        progress: int | float = 0,
        total: int | float = 100,
        icon: str = "",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.progress = progress
        self.total = total
        self.icon = icon

    @override
    def compose(self) -> ComposeResult:
        yield Label(self.icon, id="icon")
        yield InlineVerticalProgressBar(self.progress, self.total, id="pb")
        yield Label(str(self.progress), id="label")

    def update(self, progress: int | float) -> None:
        self.progress = progress
        self.query_one("#pb", InlineVerticalProgressBar).update(progress)
        self.query_one("#label", Label).update(str(progress))
