from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "radar_collector_state.py"


spec = importlib.util.spec_from_file_location("radar_collector_state", MODULE_PATH)
assert spec is not None
radar_collector_state = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(radar_collector_state)


class RadarCollectorStateTest(unittest.TestCase):
    def test_disables_collector_after_repeated_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "reddit-rss:LocalLLaMA"
            for _ in range(3):
                radar_collector_state.record_result(root, name, False, "403")
            self.assertTrue(radar_collector_state.is_disabled(root, name))

    def test_active_collectors_filters_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            names = ["hn:agent", "reddit-rss:test", "pypi-updates:mcp"]
            radar_collector_state.record_result(root, "reddit-rss:test", False, "403")
            radar_collector_state.record_result(root, "reddit-rss:test", False, "403")
            radar_collector_state.record_result(root, "reddit-rss:test", False, "403")
            active = radar_collector_state.active_collectors(root, names)
            self.assertIn("hn:agent", active)
            self.assertNotIn("reddit-rss:test", active)
            self.assertIn("pypi-updates:mcp", active)

    def test_rejected_repo_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            radar_collector_state.record_repo_rejection(root, "dead/project", "HTTP Error 404: Not Found")
            self.assertIn("dead/project", radar_collector_state.rejected_repos(root))
            self.assertTrue(radar_collector_state.is_disabled(root, "release:dead/project"))

    def test_env_disabled_collectors_merge_with_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.dict(os.environ, {"DISABLED_COLLECTORS": "hn:agent"}, clear=True):
                active = radar_collector_state.active_collectors(root, ["hn:agent", "pypi-updates:mcp"])
            self.assertEqual(active, ["pypi-updates:mcp"])

    def test_transient_error_triggers_degraded_backoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "bluesky:AI agent"
            radar_collector_state.record_result(root, name, True)
            radar_collector_state.record_result(root, name, False, "timeout")
            self.assertTrue(radar_collector_state.is_disabled(root, name))
            record = radar_collector_state.load_state(root)["collectors"][name]
            self.assertEqual(record["status"], "degraded")

    def test_transient_errors_enter_degraded_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "feed:github-changelog"
            radar_collector_state.record_result(root, name, False, "503 Service Unavailable")
            state = radar_collector_state.load_state(root)
            record = state["collectors"][name]
            self.assertEqual(record["status"], "degraded")
            self.assertTrue(record.get("next_retry_after"))

    def test_degraded_collector_recovers_after_ok_streak(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            name = "feed:test"
            radar_collector_state.record_result(root, name, False, "timeout")
            for _ in range(3):
                radar_collector_state.record_result(root, name, True)
            state = radar_collector_state.load_state(root)
            record = state["collectors"][name]
            self.assertEqual(record["status"], "ok")

    def test_collect_status_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            radar_collector_state.record_result(root, "hn:agent", True)
            payload = radar_collector_state.collect_status_payload(root)
            self.assertIn("collectors", payload)
            self.assertEqual(payload["disabled_count"], 0)

    def test_fallback_feed_mapping(self) -> None:
        fb = radar_collector_state.fallback_feed_for_collector("page:cursor-changelog")
        self.assertIsNotNone(fb)
        self.assertEqual(fb[0], "feed:cursor-changelog")


if __name__ == "__main__":
    unittest.main()
