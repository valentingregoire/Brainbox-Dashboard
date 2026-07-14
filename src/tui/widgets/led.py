from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from typing_extensions import override


class LED(Widget):
    # CSS_PATH: str = "led.tcss"
    DEFAULT_CSS: str = """
        LED {
            width: 7;
            height: 3;
            margin: 0 3;
            padding: 1 3;
        }
        LED.status-0 {
            background: #A0A0A0;
        }
        LED.status-1 {
            background: #27F071;
        }
        LED.status-2 {
            background: #F0A027;
        }
    """

    status: reactive[int] = reactive(0)

    def __init__(
        self, status: int = 0, id: str | None = None, classes: str = ""
    ) -> None:
        super().__init__(id=id, classes=classes)
        self.status = status

    @override
    def render(self) -> RenderResult:
        if self.status > 0:
            return str(self.status)
        return ""

    def update(self, status: int):
        self.status = status
        _ = self.remove_class("status-0")
        _ = self.remove_class("status-1")
        _ = self.remove_class("status-2")
        _ = self.add_class(f"status-{status}")
        _ = self.render()
