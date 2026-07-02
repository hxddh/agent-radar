from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "agent_radar.py"


spec = importlib.util.spec_from_file_location("agent_radar", MODULE_PATH)
assert spec is not None
agent_radar = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(agent_radar)


@contextlib.contextmanager
def chdir(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class ValidateCalendarTest(unittest.TestCase):
    def test_ensure_then_validate_passes_for_new_iso_week(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()
            with chdir(root):
                self.assertEqual(agent_radar.main(["init", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["ensure", "--date", "2026-07-06"]), 0)
                self.assertEqual(agent_radar.main(["validate", "--date", "2026-07-06"]), 0)

    def test_validate_warns_without_ensure_for_missing_weekly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()
            with chdir(root):
                agent_radar.main(["init", "--date", "2026-07-02"])
                agent_radar.main(["daily", "--date", "2026-07-06"])
                exit_code = agent_radar.main(["validate", "--date", "2026-07-06"])
            self.assertEqual(exit_code, 0)

    def test_validate_fails_without_daily_month_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()
            with chdir(root):
                agent_radar.main(["init", "--date", "2026-07-02"])
                agent_radar.main(["daily", "--date", "2026-07-02"])
                (root / "daily" / "2026-07.md").unlink()
                self.assertEqual(agent_radar.main(["validate", "--date", "2026-07-02"]), 1)

    def test_bilingual_warning_on_english_only_weekly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()
            with chdir(root):
                agent_radar.main(["init", "--date", "2026-07-02"])
                agent_radar.main(["weekly", "--date", "2026-07-02"])
            weekly = root / "weekly" / "2026-W27.md"
            weekly.write_text(
                "# Agent Radar Weekly - 2026-W27\n\n- one\n- two\n- three\n",
                encoding="utf-8",
            )
            warnings = agent_radar.warn_bilingual_missing(weekly)
            self.assertTrue(any("bilingual" in item for item in warnings))

    def test_year_simulation_most_days_pass_after_ensure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()
            with chdir(root):
                agent_radar.main(["init", "--date", "2026-07-02"])
                passed = 0
                for i in range(120):
                    day = dt.date(2026, 7, 2) + dt.timedelta(days=i)
                    agent_radar.ensure_reports(root, day)
                    if agent_radar.main(["validate", "--date", day.isoformat()]) == 0:
                        passed += 1
                self.assertGreater(passed, 110)


if __name__ == "__main__":
    unittest.main()
