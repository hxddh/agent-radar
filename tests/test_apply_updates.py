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
                    {"updates": [{"path": "radar.md", "mode": "append", "content": "# Radar\n"}]},
                )

    def test_rejects_full_update_for_structure_preserved_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "research-log.md"
            target.write_text("# Research Log\n\n## 2026-07-02\n\n- item\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                cloud_agent_runner.apply_updates(
                    root,
                    ["research-log.md"],
                    {"updates": [{"path": "research-log.md", "mode": "full", "content": "# Research Log\n\n- only bullets\n"}]},
                )

    def test_rejects_suspiciously_short_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "weekly" / "2026-W27.md"
            target.parent.mkdir(parents=True)
            target.write_text("x\n" * 600, encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["weekly/2026-W27.md"],
                    {"updates": [{"path": "weekly/2026-W27.md", "mode": "full", "content": "tiny\n"}]},
                )
            self.assertIn("replace_section", str(ctx.exception))

    def test_rejects_full_update_for_existing_weekly_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "weekly" / "2026-W28.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# Weekly\n\n## English\n\n### 1. Executive Summary\n\n- old summary\n\n---\n\n## 中文\n\n### 1. Executive Summary\n\n- 旧摘要\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["weekly/2026-W28.md"],
                    {
                        "updates": [
                            {
                                "path": "weekly/2026-W28.md",
                                "mode": "full",
                                "content": "# Weekly\n\n## English\n\n### 1. Executive Summary\n\n- new summary\n",
                            }
                        ]
                    },
                )
            self.assertIn("replace_section", str(ctx.exception))

    def test_rejects_full_update_for_existing_monthly_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "monthly" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Monthly\n\n## English\n\n- old thesis\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["monthly/2026-07.md"],
                    {"updates": [{"path": "monthly/2026-07.md", "mode": "full", "content": "# Monthly\n\n## English\n\n- new thesis\n"}]},
                )
            self.assertIn("replace_section", str(ctx.exception))

    def test_weekly_replace_section_updates_subsection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "weekly" / "2026-W28.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# Weekly\n\n## English\n\n### 15. Changed Thesis\n\n- old thesis\n\n### 16. Watch Next Week\n\n- old watch\n",
                encoding="utf-8",
            )
            changed = cloud_agent_runner.apply_updates(
                root,
                ["weekly/2026-W28.md"],
                {
                    "updates": [
                        {
                            "path": "weekly/2026-W28.md",
                            "mode": "replace_section",
                            "anchor": "### 15. Changed Thesis",
                            "content": "- new thesis point\n",
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertIn("- new thesis point", text)
            self.assertNotIn("- old thesis", text)
            self.assertIn("### 16. Watch Next Week", text)

    def test_allows_append_style_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "research-log.md"
            original = "# Research Log\n\n## 2026-07-02\n\n- item\n"
            target.write_text(original, encoding="utf-8")
            changed = cloud_agent_runner.apply_updates(
                root,
                ["research-log.md"],
                {
                    "updates": [
                        {
                            "path": "research-log.md",
                            "mode": "append",
                            "content": "\n## 2026-07-03\n\n- new item\n",
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            self.assertIn("2026-07-03", target.read_text(encoding="utf-8"))

    def test_replace_section_updates_anchor_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "radar.md"
            target.write_text(
                "# Radar\n\n## Current thesis\n\n- old point\n\n## Open questions\n\n- q1\n",
                encoding="utf-8",
            )
            changed = cloud_agent_runner.apply_updates(
                root,
                ["radar.md"],
                {
                    "updates": [
                        {
                            "path": "radar.md",
                            "mode": "replace_section",
                            "anchor": "## Current thesis",
                            "content": "- new point\n",
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertIn("- new point", text)
            self.assertNotIn("- old point", text)
            self.assertIn("## Open questions", text)

    def test_rejects_legacy_files_for_existing_weekly_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "weekly" / "2026-W28.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Weekly\n\n## English\n\n- existing\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["weekly/2026-W28.md"],
                    {"files": [{"path": "weekly/2026-W28.md", "content": "# Weekly\n\n## English\n\n- new\n"}]},
                )
            self.assertIn("legacy files[]", str(ctx.exception))

    def test_rejects_legacy_files_for_existing_daily_month_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Daily\n\n## 2026-07-01\n\n- old\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {"files": [{"path": "daily/2026-07.md", "content": "# Daily\n\n## 2026-07-02\n\n- new\n"}]},
                )
            self.assertIn("legacy files[]", str(ctx.exception))

    def test_replace_section_within_scopes_bilingual_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "weekly" / "2026-W28.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# Weekly\n\n## English\n\n### 15. Changed Thesis\n\n- english old\n\n---\n\n"
                "## 中文\n\n### 15. Changed Thesis\n\n- 中文旧\n",
                encoding="utf-8",
            )
            changed = cloud_agent_runner.apply_updates(
                root,
                ["weekly/2026-W28.md"],
                {
                    "updates": [
                        {
                            "path": "weekly/2026-W28.md",
                            "mode": "replace_section",
                            "within": "## 中文",
                            "anchor": "### 15. Changed Thesis",
                            "content": "- 中文新\n",
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertIn("- english old", text)
            self.assertIn("- 中文新", text)
            self.assertNotIn("- 中文旧", text)

    def test_rejects_invalid_daily_heading_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Daily\n\n## 2026-07-01\n\n- old\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {
                        "updates": [
                            {
                                "path": "daily/2026-07.md",
                                "mode": "append",
                                "content": "\n## 2026-07-02 (Screening Pass)\n\n- new\n",
                            }
                        ]
                    },
                )
            self.assertIn("exactly ## YYYY-MM-DD", str(ctx.exception))

    def test_coerces_duplicate_daily_append_to_replace_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# Daily\n\n## 2026-07-04\n\n### English\n\n- Signal: shell\n\n### 中文\n\n- 信号：占位\n",
                encoding="utf-8",
            )
            changed = cloud_agent_runner.apply_updates(
                root,
                ["daily/2026-07.md"],
                {
                    "updates": [
                        {
                            "path": "daily/2026-07.md",
                            "mode": "append",
                            "content": (
                                "\n---\n\n## 2026-07-04\n\n### English\n\n- Signal: updated content here.\n\n"
                                "### 中文\n\n- 信号：更新后的中文内容。\n"
                            ),
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertEqual(text.count("## 2026-07-04"), 1)
            self.assertIn("updated content here", text)
            self.assertNotIn("shell", text)

    def test_replace_section_strips_day_heading_from_body(self) -> None:
        """Models often put ## YYYY-MM-DD inside replace_section content; strip it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# Daily\n\n## 2026-07-09\n\n### English\n\n- Signal: shell\n\n### 中文\n\n- 信号：占位\n",
                encoding="utf-8",
            )
            changed = cloud_agent_runner.apply_updates(
                root,
                ["daily/2026-07.md"],
                {
                    "updates": [
                        {
                            "path": "daily/2026-07.md",
                            "mode": "replace_section",
                            "anchor": "## 2026-07-09",
                            "content": (
                                "## 2026-07-09\n\n### English\n\n"
                                "- Signal: Anthropic containment note.\n\n"
                                "### 中文\n\n"
                                "- 信号：Anthropic 隔离说明。\n"
                            ),
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertEqual(text.count("## 2026-07-09"), 1)
            self.assertIn("Anthropic containment", text)
            self.assertNotIn("shell", text)

    def test_rejects_append_spanning_multiple_existing_days(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Daily\n\n## 2026-07-02\n\n- existing\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {
                        "updates": [
                            {
                                "path": "daily/2026-07.md",
                                "mode": "append",
                                "content": (
                                    "\n## 2026-07-02\n\n- duplicate day\n\n"
                                    "## 2026-07-05\n\n- another day\n"
                                ),
                            }
                        ]
                    },
                )
            self.assertIn("already exists", str(ctx.exception))

    def test_legacy_files_array_still_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "weekly" / "2026-W27.md"
            target.parent.mkdir(parents=True)
            changed = cloud_agent_runner.apply_updates(
                root,
                ["weekly/2026-W27.md"],
                {"files": [{"path": "weekly/2026-W27.md", "content": "# Weekly\n\n## English\n\n- item\n\n---\n\n## 中文\n\n- 条目\n"}]},
            )
            self.assertEqual(changed, 1)

    def test_rejects_full_update_for_existing_daily_month_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# Daily Agent Radar - 2026-07\n\n## 2026-07-01\n\n### English\n\n- Signal: old day\n",
                encoding="utf-8",
            )
            content = (
                "# Daily Agent Radar - 2026-07\n\n## 2026-07-01\n\n### English\n\n- Signal: old day\n\n"
                "## 2026-07-02\n\n### English\n\n- Signal: new day\n"
            )
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {"updates": [{"path": "daily/2026-07.md", "mode": "full", "content": content}]},
                )
            self.assertIn("append a new ## YYYY-MM-DD", str(ctx.exception))

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
                    {"updates": [{"path": "daily/2026-07.md", "mode": "full", "content": "# Daily\n\n## 2026-07-02\n\n- new\n"}]},
                )

    def test_rejects_report_without_cjk_chinese(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = (
                "# Daily Agent Radar - 2026-07\n\n## 2026-07-02\n\n"
                + "".join(
                    f"- 中文：\n- English: filler english line number {index}.\n"
                    for index in range(12)
                )
            )
            with self.assertRaises(SystemExit):
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {"updates": [{"path": "daily/2026-07.md", "mode": "full", "content": content}]},
                )

    def test_bilingualizes_daily_report_updates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            changed = cloud_agent_runner.apply_updates(
                root,
                ["daily/2026-07.md"],
                {
                    "updates": [
                        {
                            "path": "daily/2026-07.md",
                            "mode": "full",
                            "content": "# Daily Agent Radar - 2026-07\n\n## 2026-07-02\n\n- one\n- two\n- three\n",
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = (root / "daily" / "2026-07.md").read_text(encoding="utf-8")
            self.assertIn("### English", text)
            self.assertIn("### 中文", text)
            self.assertIn("one", text)

    def test_rejects_oversized_daily_append(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "daily" / "2026-07.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Daily\n\n## 2026-07-02\n\n- existing\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["daily/2026-07.md"],
                    {
                        "updates": [
                            {
                                "path": "daily/2026-07.md",
                                "mode": "append",
                                "content": "\n\n## 2026-07-03\n\n" + ("x" * 24_000),
                            }
                        ]
                    },
                )
            self.assertIn("MAX_DAILY_APPEND_CHARS", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
