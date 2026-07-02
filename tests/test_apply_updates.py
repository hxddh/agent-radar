from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "cloud_agent_runner.py"


spec = importlib.util.spec_from_file_location("cloud_agent_runner", MODULE_PATH)
assert spec is not None
cloud_agent_runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cloud_agent_runner)


class ApplyUpdatesTest(unittest.TestCase):
    def test_rejects_non_allowed_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(SystemExit):
                cloud_agent_runner.apply_updates(
                    root,
                    ["research-log.md"],
                    {"files": [{"path": "radar.md", "content": "# Radar\n"}]},
                )

    def test_rejects_suspiciously_short_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "research-log.md"
            target.write_text("x\n" * 600, encoding="utf-8")
            with self.assertRaises(SystemExit):
                cloud_agent_runner.apply_updates(
                    root,
                    ["research-log.md"],
                    {"files": [{"path": "research-log.md", "content": "tiny\n"}]},
                )

    def test_allows_append_style_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "research-log.md"
            original = "# Research Log\n\n## 2026-07-02\n\n- item\n"
            target.write_text(original, encoding="utf-8")
            updated = original + "\n## 2026-07-03\n\n- new item\n"
            changed = cloud_agent_runner.apply_updates(
                root,
                ["research-log.md"],
                {"files": [{"path": "research-log.md", "content": updated}]},
            )
            self.assertEqual(changed, 1)
            self.assertIn("2026-07-03", target.read_text(encoding="utf-8"))


    def test_rejects_missing_structure_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "research-log.md"
            target.write_text("# Research Log\n\n## 2026-07-02\n\n- item\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                cloud_agent_runner.apply_updates(
                    root,
                    ["research-log.md"],
                    {"files": [{"path": "research-log.md", "content": "# Research Log\n\n- only bullets\n"}]},
                )

    def test_rejects_missing_daily_dates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Daily\n\n## 2026-07-01\n\n- old\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {"files": [{"path": "daily/2026-07.md", "content": "# Daily\n\n## 2026-07-02\n\n- new\n"}]},
                )

    def test_bilingualizes_daily_report_updates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            changed = cloud_agent_runner.apply_updates(
                root,
                ["daily/2026-07.md"],
                {
                    "files": [
                        {
                            "path": "daily/2026-07.md",
                            "content": "# Daily Agent Radar - 2026-07\n\n## 2026-07-02\n\n- one\n- two\n- three\n",
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = (root / "daily" / "2026-07.md").read_text(encoding="utf-8")
            self.assertIn("中文：", text)
            self.assertIn("English:", text)


if __name__ == "__main__":
    unittest.main()
