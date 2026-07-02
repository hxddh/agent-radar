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

    def test_bilingualize_adds_markers(self) -> None:
        content = "# Agent Radar Weekly - 2026-W27\n\n- one signal\n- two signal\n- three signal\n"
        updated = radar_bilingual.bilingualize_report(content)
        self.assertIn("中文：", updated)
        self.assertIn("English:", updated)

    def test_ensure_bilingual_skips_non_report_paths(self) -> None:
        content = "# Research Log\n\n- item\n"
        self.assertEqual(
            radar_bilingual.ensure_bilingual_file_content("research-log.md", content),
            content,
        )

    def test_already_bilingual_content_is_unchanged(self) -> None:
        content = "# Agent Radar Weekly - 2026-W27\n\n- 中文：signal\n- English: signal\n"
        self.assertFalse(radar_bilingual.needs_bilingual(content))


if __name__ == "__main__":
    unittest.main()
