from unittest.mock import patch

from main import BrainboxDashboard
from service import telemetry_mock


@patch("main.telemetry", telemetry_mock)
class TestBrainboxDashboard:
    async def test_bla(self) -> None:

        app = BrainboxDashboard()
        async with app.run_test() as pilot:
            _ = await pilot.click("#btn_close")

    # async def test_bla(self) -> None:
    #     app = BrainboxDashboard()
    #     async with app.run_test() as pilot:
    #         _ = await pilot.click("#volume_control")
    #         assert app.screen.id == "sound"
