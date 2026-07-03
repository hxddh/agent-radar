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
        self.assertTrue(radar_bilingual.is_block_bilingual_format(updated))
        self.assertIn("## English", updated)
        self.assertIn("## 中文", updated)
        self.assertIn("one signal", updated)

    def test_block_format_substance_counts(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W28\n\n"
            "> Format note\n\n"
            "## English\n\n"
            "### 1. Executive Summary\n\n"
            "- English summary line one with enough substance.\n"
            "- English summary line two with enough substance.\n"
            "- English summary line three with enough substance.\n\n"
            "---\n\n"
            "## 中文\n\n"
            "### 1. Executive Summary\n\n"
            "- 第一条中文摘要内容足够长。\n"
            "- 第二条中文摘要内容足够长。\n"
            "- 第三条中文摘要内容足够长。\n"
        )
        self.assertTrue(radar_bilingual.is_block_bilingual_format(content))
        self.assertEqual(radar_bilingual.substantive_english_lines(content), 3)
        self.assertEqual(radar_bilingual.substantive_chinese_cjk_lines(content), 3)
        self.assertFalse(radar_bilingual.missing_chinese_substance(content))

    def test_convert_paired_to_block(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "## 1. Executive Summary\n\n"
            "- Signal\n"
            "  - 中文：苹果发布 MCP 服务器。\n"
            "  - English: Apple shipped an MCP server.\n"
        )
        converted = radar_bilingual.convert_paired_to_block(content)
        self.assertTrue(radar_bilingual.is_block_bilingual_format(converted))
        self.assertIn("Apple shipped an MCP server.", converted)
        self.assertIn("苹果发布 MCP 服务器。", converted)
        self.assertNotIn("中文：", converted)

    def test_ensure_bilingual_converts_weekly_paired_to_block(self) -> None:
        content = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "- 中文：信号\n- English: signal\n"
        )
        updated = radar_bilingual.ensure_bilingual_file_content("weekly/2026-W27.md", content)
        self.assertTrue(radar_bilingual.is_block_bilingual_format(updated))

    def test_convert_daily_paired_preserves_field_structure(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-07-02\n\n"
            "### 1. New Signals\n\n"
            "- Signal\n"
            "  - 中文：测试信号。\n"
            "  - English: Test signal.\n"
            "  - What happened\n"
            "    - 中文：发生了某事。\n"
            "    - English: Something happened.\n"
            "  - Why it matters\n"
            "    - 中文：这很重要。\n"
            "    - English: This matters.\n"
            "  - Source: https://example.com/changelog\n"
        )
        converted = radar_bilingual.convert_daily_paired_to_block(content)
        self.assertIn("  - What happened: Something happened.", converted)
        self.assertIn("  - Why it matters: This matters.", converted)
        self.assertIn(radar_bilingual.CHINESE_SOURCE_INDEX.split("：")[0], converted)
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-07-02\n\n"
            "- Signal\n"
            "  - 中文：测试信号。\n"
            "  - English: Test signal.\n"
        )
        updated = radar_bilingual.ensure_bilingual_file_content("daily/2026-07.md", content)
        self.assertTrue(radar_bilingual.is_daily_block_format(updated))
        self.assertIn("### English", updated)
        self.assertIn("### 中文", updated)
        self.assertNotIn("中文：", updated)

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

    def test_collapse_empty_chinese_label_url_pair(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "  - Sources:\n"
            "    - 中文：\n"
            "    - English: BrainRouter: https://github.com/kinqsradiollc/BrainRouter\n"
        )
        repaired = radar_bilingual.repair_identical_bilingual_pairs(content)
        self.assertIn("- BrainRouter: https://github.com/kinqsradiollc/BrainRouter\n", repaired)
        self.assertEqual(radar_bilingual.empty_chinese_label_lines(repaired), 0)

    def test_empty_chinese_label_lines_counted(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "    - 中文：\n"
            "    - English: filler english line number one.\n"
        )
        self.assertEqual(radar_bilingual.empty_chinese_label_lines(content), 1)

    def test_ensure_bilingual_skips_non_report_paths(self) -> None:
        content = "# Research Log\n\n- item\n"
        self.assertEqual(
            radar_bilingual.ensure_bilingual_file_content("research-log.md", content),
            content,
        )

    def test_already_bilingual_content_is_unchanged(self) -> None:
        content = "# Agent Radar Weekly - 2026-W27\n\n- 中文：信号\n- English: signal\n"
        self.assertFalse(radar_bilingual.needs_bilingual(content))

    def test_assemble_daily_day_block(self) -> None:
        block = radar_bilingual.assemble_daily_day_block(
            "#### 1. Signals\n\n- Signal: test\n",
            "#### 1. Signals\n\n- 信号：测试\n",
            "## 2026-07-03",
        )
        self.assertIn("### English", block)
        self.assertIn("### 中文", block)
        self.assertIn("## 2026-07-03", block)

    def test_daily_block_lighter_chinese_gate(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-07-03\n\n"
            "### English\n\n"
            "#### 1. Signals\n\n- Signal: one with enough english substance here.\n"
            "#### 2. Signals\n\n- Signal: two with enough english substance here.\n"
            "#### 3. Signals\n\n- Signal: three with enough english substance here.\n\n"
            "### 中文\n\n"
            "#### 1. Signals\n\n- 信号：第一条中文内容。\n"
            "#### 2. Signals\n\n- 信号：第二条中文内容。\n"
            "#### 3. Signals\n\n- 信号：第三条中文内容。\n"
        )
        self.assertTrue(radar_bilingual.is_daily_block_format(content))
        self.assertFalse(radar_bilingual.missing_chinese_substance_daily_block(content))

    def test_bilingual_char_stats_daily(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-07-03\n\n"
            "### English\n\n- English text here.\n\n"
            "### 中文\n\n- 中文内容在这里。\n"
        )
        stats = radar_bilingual.bilingual_char_stats(content)
        self.assertGreater(stats["english_chars"], 0)
        self.assertGreater(stats["chinese_cjk_chars"], 0)


if __name__ == "__main__":
    unittest.main()
