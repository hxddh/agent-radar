from __future__ import annotations

import importlib.util
import tempfile
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

    def test_missing_chinese_requires_cjk_not_english_copy(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            + "".join(
                f"- 中文：English only line number {index}.\n- English: English only line number {index}.\n"
                for index in range(12)
            )
        )
        self.assertTrue(radar_bilingual.missing_chinese_substance(content))

    def test_token_chinese_no_longer_satisfies_substance_check(self) -> None:
        # 3 real Chinese lines against 11 substantive English lines is token
        # coverage, not a bilingual report; the proportional rule flags it.
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "- 中文：浏览器工具进入主流产品。\n- English: Browser tools are mainstream.\n"
            "- 中文：沙箱执行成为基础设施信号。\n- English: Sandbox execution is an infra signal.\n"
            "- 中文：存储面包括日志与 trace。\n- English: Storage surfaces include logs and traces.\n"
            + "".join(
                f"- 中文：\n- English: filler english line number {index}.\n"
                for index in range(8)
            )
        )
        self.assertTrue(radar_bilingual.missing_chinese_substance(content))

    def test_proportional_chinese_coverage_satisfies_substance_check(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            + "".join(
                f"- 中文：这是第 {index} 条真实的中文双语内容行。\n"
                f"- English: This is real bilingual content line number {index}.\n"
                for index in range(9)
            )
            + "".join(
                f"- 中文：\n- English: filler english line number {index}.\n"
                for index in range(3)
            )
        )
        # 9 real Chinese lines / 12 substantive English lines = 75% >= 60%.
        self.assertFalse(radar_bilingual.missing_chinese_substance(content))

    def test_url_lines_do_not_count_as_substantive_english(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            + "".join(
                f"- English: https://example.com/very/long/path/item-{index}\n"
                for index in range(20)
            )
        )
        self.assertEqual(radar_bilingual.substantive_english_lines(content), 0)
        self.assertFalse(radar_bilingual.missing_chinese_substance(content))

    def test_repair_collapses_identical_url_pair_to_single_line(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "- 中文：https://example.com/changelog\n"
            "- English: https://example.com/changelog\n"
        )
        repaired = radar_bilingual.repair_identical_bilingual_pairs(content)
        self.assertIn("- https://example.com/changelog\n", repaired)
        self.assertNotIn("中文：https://example.com/changelog", repaired)
        self.assertNotIn("English: https://example.com/changelog", repaired)

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
