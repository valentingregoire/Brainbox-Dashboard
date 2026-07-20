from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from typing_extensions import override

from . import CLR_OK, CLR_TEXT_OK, CLR_TEXT_WARN, CLR_WARN


class LED(Widget):
    DEFAULT_CSS: str = f"""
        LED {{
            width: 7;
            height: 3;
            margin: 0 3;
            padding: 1 3;
            text-style: bold;
        }}
        LED.status-0 {{
            background: #A0A0A0;
        }}
        LED.status-1 {{
            background: {CLR_OK};
            color: {CLR_TEXT_OK};

        }}
        LED.status-2 {{
            background: {CLR_WARN};
            color: {CLR_TEXT_WARN};
        }}
    """  # ty:ignore[invalid-attribute-override]

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
