from textual.app import RenderResult
from textual.widgets import Static
from typing_extensions import override


class Separator(Static):
    DEFAULT_CSS: str = """
    Separator {
        width: 1;
        height: 1;
        color: #555555;
    }
    """

    @override
    def render(self) -> RenderResult:
        return "|"
        # return "┃"
