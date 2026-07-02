from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "radar_bilingual.py"


spec = importlib.util.spec_from_file_location("radar_bilingual", MODULE_PATH)
assert spec is not None
radar_bilingual = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(radar_bilingual)


class RadarBilingualTest(unittest.TestCase):
    def test_needs_bilingual_for_english_only_report(self) -> None:
        content = "# Agent Radar Weekly - 2026-W27\n\n- one\n- two\n- three\n"
        self.assertTrue(radar_bilingual.needs_bilingual(content))

    def test_bilingualize_adds_empty_chinese_placeholder(self) -> None:
        content = "# Agent Radar Weekly - 2026-W27\n\n- one signal\n- two signal\n- three signal\n"
        updated = radar_bilingual.bilingualize_report(content)
        self.assertIn("中文：", updated)
        self.assertIn("English: one signal", updated)
        self.assertNotIn("中文：one signal", updated)

    def test_identical_pairs_detected(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "- 中文：This is a duplicated bilingual sentence for testing.\n"
            "- English: This is a duplicated bilingual sentence for testing.\n"
        )
        self.assertEqual(len(radar_bilingual.identical_bilingual_pairs(content)), 1)

    def test_repair_clears_identical_chinese_line(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "- 中文：This is a duplicated bilingual sentence for testing.\n"
            "- English: This is a duplicated bilingual sentence for testing.\n"
        )
        repaired = radar_bilingual.repair_identical_bilingual_pairs(content)
        self.assertIn("- 中文：\n", repaired)
        self.assertEqual(len(radar_bilingual.identical_bilingual_pairs(repaired)), 0)

    def test_ensure_bilingual_skips_non_report_paths(self) -> None:
        content = "# Research Log\n\n- item\n"
        self.assertEqual(
            radar_bilingual.ensure_bilingual_file_content("research-log.md", content),
            content,
        )

    def test_already_bilingual_content_is_unchanged(self) -> None:
        content = "# Agent Radar Weekly - 2026-W27\n\n- 中文：信号\n- English: signal\n"
        self.assertFalse(radar_bilingual.needs_bilingual(content))


if __name__ == "__main__":
    unittest.main()
