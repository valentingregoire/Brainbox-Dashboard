from textual.app import RenderResult
from textual.widgets import Static
from typing_extensions import override


class InlineButton(Static):
    """A simple button of 1 height."""

    DEFAULT_CSS: str = """
    InlineButton {
        width: 4;
        height: 1;
        # margin: 0 1;
        # padding: 0 1;
        text-align: center;
        # border-left: solid red;
        # border-right: solid red;
    }
    """

    @override
    def __init__(self, label: str | None = None, id: str | None = None) -> None:
        super().__init__(id=id)
        self.label: str | None = label

    @override
    def render(self) -> RenderResult:
        return self.label or ""
