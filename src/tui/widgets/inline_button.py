from textual.app import RenderResult
from textual.message import Message
from textual.widgets import Static
from typing_extensions import override


class InlineButton(Static):
    class Clicked(Message):
        def __init__(self) -> None:
            super().__init__()

    DEFAULT_CSS: str = """
    InlineButton {
        width: 5;
        height: 1;
        # margin: 0 1;
        padding: 0 1;
        text-align: center;
    }
    """

    @override
    def __init__(self, label: str | None = None, id: str | None = None) -> None:
        super().__init__(id=id)
        self.label: str | None = label

    @override
    def render(self) -> RenderResult:
        return self.label or ""

    def on_click(self) -> None:
        _ = self.post_message(self.Clicked())
