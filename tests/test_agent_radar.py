from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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


class AgentRadarCliTest(unittest.TestCase):
    def test_daily_weekly_monthly_validate_and_root_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()

            with chdir(root):
                self.assertEqual(agent_radar.main(["init", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["ensure", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["daily", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["daily", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["weekly", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["monthly", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["validate", "--date", "2026-07-02"]), 0)
                self.assertEqual(agent_radar.main(["release-draft", "--date", "2026-07-02"]), 0)

            daily = root / "daily" / "2026-07.md"
            weekly = root / "weekly" / "2026-W27.md"
            monthly = root / "monthly" / "2026-07.md"
            release_draft = root / "docs" / "release-draft.md"

            self.assertTrue(daily.exists())
            self.assertTrue(weekly.exists())
            self.assertTrue(monthly.exists())
            self.assertTrue(release_draft.exists())
            self.assertTrue((root / "automation" / "source-health.md").exists())
            self.assertTrue((root / "automation" / "source-lanes.md").exists())
            self.assertTrue((root / "automation" / "telemetry" / ".gitkeep").exists())
            self.assertTrue((root / "docs" / "architecture.md").exists())
            self.assertTrue((root / "docs" / "release-checklist.md").exists())
            self.assertEqual(daily.read_text(encoding="utf-8").count("## 2026-07-02"), 1)
            self.assertIn("### English", daily.read_text(encoding="utf-8"))
            self.assertIn("### 中文", daily.read_text(encoding="utf-8"))
            self.assertIn("## English", weekly.read_text(encoding="utf-8"))
            self.assertIn("## 中文", weekly.read_text(encoding="utf-8"))
            self.assertIn("## English", monthly.read_text(encoding="utf-8"))
            self.assertIn("## 中文", monthly.read_text(encoding="utf-8"))

            nested = root / "daily" / "nested"
            nested.mkdir()
            with chdir(nested):
                detected = agent_radar.find_root()
            self.assertEqual(detected.resolve(), root.resolve())

    def test_invalid_date_exits(self) -> None:
        with self.assertRaises(SystemExit):
            agent_radar.parse_date("2026-99-99")

    def test_trigger_cloud_agent_uses_repository_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "radar.md").write_text("# radar\n", encoding="utf-8")
            (root / "agent-watchlist.md").write_text("# watchlist\n", encoding="utf-8")
            with chdir(root):
                with mock.patch.object(agent_radar, "github_token", return_value="test-token"):
                    with mock.patch.object(agent_radar, "github_repo_slug", return_value="owner/repo"):
                        with mock.patch.object(agent_radar, "repository_dispatch") as dispatch:
                            code = agent_radar.main(
                                ["trigger", "cloud-agent", "--task", "daily", "--date", "2026-07-02"]
                            )
            self.assertEqual(code, 0)
            dispatch.assert_called_once_with(
                "owner/repo",
                "test-token",
                "cloud-agent",
                {"task": "daily", "date": "2026-07-02"},
            )

    def test_trigger_requires_token(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "radar.md").write_text("# radar\n", encoding="utf-8")
            (root / "agent-watchlist.md").write_text("# watchlist\n", encoding="utf-8")
            with chdir(root):
                with mock.patch.object(agent_radar, "github_token", return_value=""):
                    code = agent_radar.main(["trigger", "validate", "--date", "2026-07-02"])
            self.assertEqual(code, 1)

    def test_brief_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "radar.md").write_text("# radar\n", encoding="utf-8")
            (root / "agent-watchlist.md").write_text("# watchlist\n", encoding="utf-8")
            with chdir(root):
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    code = agent_radar.main(["brief", "--date", "2026-07-03", "--json"])
            self.assertEqual(code, 0)
            payload = json.loads(buffer.getvalue())
            self.assertEqual(payload["date"], "2026-07-03")
            self.assertIn("recent_telemetry", payload)


if __name__ == "__main__":
    unittest.main()
