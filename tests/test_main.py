from unittest.mock import patch

from textual.messages import ExitApp

from main import BrainboxDashboard
from service.telemetry_mock import TelemetryMock
from tui.widgets.led import LED
from tui.widgets.status import Status
from tui.widgets.volume_control import VolumeControl

telemetry: TelemetryMock = TelemetryMock()


@patch("main.Telemetry", lambda: telemetry)
class TestSoundScreen:
    async def test_sound_volume_controls(self) -> None:
        app = BrainboxDashboard()
        initial_volume: int = telemetry.get_volume()
        max_volume: int = telemetry.max_volume
        async with app.run_test() as pilot:
            _ = await pilot.click("#volume_control")
            assert app.screen.id == "sound_screen"

            _ = await pilot.click("#vol_plus")
            assert telemetry.get_volume() == round(
                initial_volume + max_volume / 20
            )

            _ = await pilot.click("#vol_min")
            assert telemetry.get_volume() == initial_volume


@patch("main.Telemetry", lambda: telemetry)
class TestStatusBar:
    class MockApp(BrainboxDashboard):
        """A testing app."""

        def __init__(self) -> None:
            super().__init__()
            self.close_message: ExitApp | None = None

        def on_exit_app(self, message: ExitApp) -> None:
            self.close_message = message

    async def test_close_btn(self) -> None:
        """Tests clicking the close button."""
        app = self.MockApp()
        async with app.run_test() as pilot:
            _ = await pilot.click("#btn_close")
            app.log(f"return: {app.return_value}")
            assert app.close_message is not None
            assert app.return_code == -1

    async def test_update_values(self) -> None:
        """Tests updating the values."""
        app = BrainboxDashboard()
        async with app.run_test() as _:
            app.update_values()
            assert (
                app.query_one("#cpu", Status).progress == telemetry.cpu_load()
            )
            assert (
                app.query_one("#ram", Status).progress
                == telemetry.memory_load()
            )
            assert (
                app.query_one("#temp", Status).progress == telemetry.cpu_temp()
            )
            assert (
                app.query_one("#fan", Status).progress == telemetry.fan_speed()
            )
            assert app.query_one(
                "#mod_host", Status
            ).progress == telemetry.mod_service_status("modep-mod-host")
            assert app.query_one(
                "#mod_ui", Status
            ).progress == telemetry.mod_service_status("modep-mod-ui")
            assert (
                app.query_one("#volume_control", VolumeControl).volume
                == telemetry.get_volume()
            )
            assert "status-0" in app.query_one("#led1", LED).classes
            assert "status-0" in app.query_one("#led2", LED).classes
            assert "status-0" in app.query_one("#led3", LED).classes
            assert "status-1" in app.query_one("#led4", LED).classes
            telemetry.current_snapshot_name = "seven"
            app.update_values()
            assert "status-0" not in app.query_one("#led4", LED).classes
            assert "status-1" not in app.query_one("#led4", LED).classes
            assert "status-2" in app.query_one("#led4", LED).classes

    async def test_update_connections(self) -> None:
        """Tests the connected devices."""
        app = BrainboxDashboard()
        async with app.run_test() as _:
            app.update_connections()
            assert app.query_one("#footswitch", Status).progress
            assert app.query_one("#tablet", Status).progress
            assert app.query_one("#laptop", Status).progress
            assert not app.query_one("#intruder", Status).progress
