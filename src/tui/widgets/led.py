from textual.app import RenderResult
from textual.reactive import reactive
from textual.widgets import Static
from typing_extensions import override


class LED(Static):
    DEFAULT_CSS: str = """
    LED {
        width: 2;
        height: 1;
        # border: solid red;
    }
    """

    status: reactive[int] = reactive(0)

    def __init__(self, status: int = 0, id: str | None = None) -> None:
        super().__init__(id=id)
        self.status = status

    @override
    def render(self) -> RenderResult:
        if self.status == 0:
            return "🔴"
        elif self.status == 1:
            return "🟢"
        else:
            return "🟡"
