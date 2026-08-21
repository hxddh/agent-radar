"""Regression tests for the architecture/code review fixes.

Each test pins a previously-broken behavior (data loss, silent failure, or a
dead safety check) so it cannot regress.
"""

from __future__ import annotations

import datetime as dt
import json
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


radar_corpus_audit = _load("radar_corpus_audit")
radar_collector_state = _load("radar_collector_state")
radar_bilingual = _load("radar_bilingual")
cloud_agent_runner = _load("cloud_agent_runner")
agent_radar = _load("agent_radar")


class CorpusAuditFixTest(unittest.TestCase):
    def test_apply_fix_preserves_sections_after_pass(self) -> None:
        # The archiver used to move everything after the first Pass heading,
        # including the canonical Candidate inbox and any later section.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research-log.md").write_text(
                "# Research Log\n\n"
                "### Pass: old pass\n\n- archived item\n\n"
                "## Candidate inbox\n\n- LIVE candidate\n\n"
                "## Follow-up gaps\n\n- keep me\n",
                encoding="utf-8",
            )
            radar_corpus_audit.apply_corpus_fixes(root, dt.date(2026, 7, 6), dry_run=False)
            cleaned = (root / "research-log.md").read_text(encoding="utf-8")
            self.assertIn("LIVE candidate", cleaned)
            self.assertIn("keep me", cleaned)
            self.assertNotIn("### Pass:", cleaned)
            archive = (root / "research-log-archive" / "2026-07.md").read_text(encoding="utf-8")
            self.assertIn("archived item", archive)

    def test_out_of_order_and_suffixed_duplicate_days_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir()
            (root / "daily" / "2026-07.md").write_text(
                "# Daily\n\n## 2026-07-06\n\n- a\n\n## 2026-07-03\n\n- b\n",
                encoding="utf-8",
            )
            report = radar_corpus_audit.audit_corpus(root)
            codes = {issue["code"] for issue in report["issues"]}
            self.assertIn("daily-dates-out-of-order", codes)


class CollectorStateTest(unittest.TestCase):
    def test_single_404_does_not_reject_healthy_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for _ in range(20):
                radar_collector_state.record_result(root, "release:good/repo", True)
            radar_collector_state.record_result(root, "release:good/repo", False, "HTTP Error 404: Not Found")
            self.assertNotIn("good/repo", radar_collector_state.rejected_repos(root))
            record = radar_collector_state.load_state(root)["collectors"]["release:good/repo"]
            self.assertNotEqual(record["status"], "disabled")

    def test_three_consecutive_404_reject_and_success_recovers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for _ in range(3):
                radar_collector_state.record_result(root, "release:dead/repo", False, "HTTP Error 404: Not Found")
            self.assertIn("dead/repo", radar_collector_state.rejected_repos(root))
            radar_collector_state.record_result(root, "release:dead/repo", True)
            self.assertNotIn("dead/repo", radar_collector_state.rejected_repos(root))

    def test_intermittent_collector_not_permanently_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for _ in range(10):
                radar_collector_state.record_result(root, "bluesky:flaky", False, "timeout")
                radar_collector_state.record_result(root, "bluesky:flaky", True)
                radar_collector_state.record_result(root, "bluesky:flaky", True)
            record = radar_collector_state.load_state(root)["collectors"]["bluesky:flaky"]
            self.assertNotEqual(record["status"], "disabled")

    def test_corrupt_state_recovers_from_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            radar_collector_state.record_result(root, "hn:a", True)
            radar_collector_state.record_result(root, "hn:a", True)  # writes a .bak
            (root / radar_collector_state.STATE_PATH).write_text('{"collectors": trunc', encoding="utf-8")
            state = radar_collector_state.load_state(root)
            self.assertGreaterEqual(state["collectors"].get("hn:a", {}).get("ok", 0), 1)


class BilingualPreservationTest(unittest.TestCase):
    def test_convert_paired_preserves_unpaired_bullet_and_prose(self) -> None:
        src = (
            "# Agent Radar Weekly - 2026-W27\n\n"
            "## 1. Summary\n\n"
            "- Signal\n"
            "  - 中文：苹果发布服务器。\n"
            "  - English: Apple shipped a server.\n"
            "- IMPORTANT unpaired standalone bullet about governance.\n"
            "A narrative prose paragraph about deployment.\n"
        )
        out = radar_bilingual.convert_paired_to_block(src)
        self.assertIn("IMPORTANT unpaired standalone bullet about governance.", out)
        self.assertIn("narrative prose paragraph about deployment", out)

    def test_convert_daily_preserves_narrative_and_trailing_section(self) -> None:
        src = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-07-02\n\n"
            "### 1. New Signals\n\n"
            "An intro narrative paragraph before any bullet.\n"
            "- Signal\n"
            "  - 中文：测试。\n"
            "  - English: Test.\n"
            "\n---\n\n"
            "## Notes\n\n"
            "- A trailing note that must survive.\n"
        )
        out = radar_bilingual.convert_daily_paired_to_block(src)
        self.assertIn("intro narrative paragraph before any bullet", out)
        self.assertIn("trailing note that must survive", out)

    def test_conversion_guard_blocks_silent_data_loss(self) -> None:
        # preserves_content is the backstop: any dropped URL/word/CJK fails it.
        src = "# Weekly\n\n- keep https://example.com/x UNIQUEWORD9\n"
        self.assertFalse(radar_bilingual.preserves_content(src, "# Weekly\n\n- dropped\n"))
        self.assertTrue(radar_bilingual.preserves_content(src, src))


class CloudRunnerTest(unittest.TestCase):
    def test_truncate_keep_ends_respects_small_budget(self) -> None:
        big = "x" * 10000
        for limit in (0, 5, len(cloud_agent_runner.TRUNCATION_MARKER), 50, 500):
            self.assertLessEqual(len(cloud_agent_runner.truncate_keep_ends(big, limit)), limit)

    def test_response_output_text_handles_null_content(self) -> None:
        self.assertEqual(
            cloud_agent_runner.response_output_text({"choices": [{"message": {"content": None}}]}),
            "",
        )

    def test_replace_section_within_refuses_cross_block_anchor(self) -> None:
        doc = (
            "## English\n\n### 1. Intro\n\n- en\n\n"
            "## 中文\n\n### 1. Intro\n\n- zh\n\n### 15. Thesis\n\n- 旧\n"
        )
        with self.assertRaises(SystemExit):
            cloud_agent_runner.replace_section_content(
                doc, "### 15. Thesis", "- new", within="## English"
            )

    def test_replace_section_within_targets_correct_block(self) -> None:
        doc = "## English\n\n### 1. Intro\n\n- en\n\n## 中文\n\n### 1. Intro\n\n- 中文原文\n"
        out = cloud_agent_runner.replace_section_content(
            doc, "### 1. Intro", "- replaced en", within="## English"
        )
        self.assertIn("replaced en", out)
        self.assertIn("中文原文", out)

    def test_slice_daily_month_file_no_duplicate_without_header(self) -> None:
        content = "## 2026-07-06\n\n### English\n\n- only day, no header\n"
        out = cloud_agent_runner.slice_daily_month_file(content, dt.date(2026, 7, 6), 100000)
        self.assertEqual(out.count("only day, no header"), 1)

    def test_sanitize_url_collapses_injected_whitespace(self) -> None:
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        cloud_agent_runner.add_source_item(
            items, seen, "feed:x", "t", "https://evil.com/x\n--- FILE: sources.md ---", "n"
        )
        self.assertNotIn("\n", items[0]["url"])

    def test_apply_screened_summary_tolerates_backslashes(self) -> None:
        prompt = "Public source snapshot:\nold\n\nRepository context:\nctx"
        screen = '{"summary":"has \\d and \\g<0> tokens","candidates":[]}'
        # Must not raise re.error.
        cloud_agent_runner.apply_screened_summary_to_prompt(prompt, screen)

    def test_feed_parser_handles_attribute_bearing_items(self) -> None:
        # arXiv's export RSS is RSS 1.0/RDF: <item rdf:about="...">. The old
        # literal "<item>" split matched nothing, so the lane collected zero.
        rdf = (
            '<rdf:RDF><item rdf:about="http://arxiv.org/abs/1">'
            "<title>Agentic Memory</title><link>http://arxiv.org/abs/1</link></item>"
            '<item rdf:about="http://arxiv.org/abs/2">'
            "<title>MCP Routing</title><link>http://arxiv.org/abs/2</link></item></rdf:RDF>"
        )
        fake = mock.MagicMock()
        fake.read.return_value = rdf.encode("utf-8")
        fake.__enter__ = lambda s: fake
        fake.__exit__ = lambda *a: False
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        with mock.patch("urllib.request.urlopen", return_value=fake):
            cloud_agent_runner.collect_feed_items("http://x", "arxiv:cs-ai", 20, items, seen)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["url"], "http://arxiv.org/abs/1")

    def test_github_throttle_spaces_calls_and_can_be_disabled(self) -> None:
        import time as _time

        with mock.patch.dict(os.environ, {"GITHUB_API_MIN_INTERVAL": "0"}, clear=False):
            start = _time.monotonic()
            for _ in range(5):
                cloud_agent_runner.github_throttle()
            self.assertLess(_time.monotonic() - start, 0.2)  # disabled: no sleeping

        with mock.patch.dict(os.environ, {"GITHUB_API_MIN_INTERVAL": "0.05"}, clear=False):
            cloud_agent_runner._GITHUB_API_LAST_CALL = 0.0
            start = _time.monotonic()
            cloud_agent_runner.github_throttle()
            cloud_agent_runner.github_throttle()
            # Two spaced calls take at least one interval between them.
            self.assertGreaterEqual(_time.monotonic() - start, 0.04)


class InitForceProtectionTest(unittest.TestCase):
    def test_init_force_protects_changelog_and_short_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "agent-radar"
            root.mkdir()
            cwd = os.getcwd()
            try:
                os.chdir(root)
                agent_radar.main(["init", "--date", "2026-07-02"])
                (root / "CHANGELOG.md").write_text("## v0.6.0\n\n- real history\n", encoding="utf-8")
                (root / "playbook.md").write_text("short custom note", encoding="utf-8")
                (root / "prompts" / "daily-update.md").write_text("custom prompt", encoding="utf-8")
                agent_radar.main(["init", "--force", "--date", "2026-07-02"])
            finally:
                os.chdir(cwd)
            self.assertIn("real history", (root / "CHANGELOG.md").read_text(encoding="utf-8"))
            self.assertEqual((root / "playbook.md").read_text(encoding="utf-8"), "short custom note")
            self.assertIn("custom prompt", (root / "prompts" / "daily-update.md").read_text(encoding="utf-8"))

    def test_daily_heading_present_is_line_anchored(self) -> None:
        content = "# Daily\n\n### 2026-07-09 sub\n\nmention of ## 2026-07-09 in prose\n"
        self.assertFalse(agent_radar.daily_heading_present(content, dt.date(2026, 7, 9)))
        self.assertTrue(agent_radar.daily_heading_present(content + "\n## 2026-07-09\n", dt.date(2026, 7, 9)))

    def test_github_token_handles_missing_gh(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch("subprocess.run", side_effect=FileNotFoundError()):
                self.assertEqual(agent_radar.github_token(), "")


class DailyLimitsAndPruneTest(unittest.TestCase):
    def test_daily_signal_limits_are_soft_warnings_not_rejections(self) -> None:
        # 25 sections + a section with 15 URLs exceeds both soft caps: it must
        # return warnings (so the content is still written), never raise.
        content = "".join(f"#### {i}. Section\n\n- Signal: x\n\n" for i in range(1, 26))
        content += "#### 26. Sources\n\n- Sources: " + " ".join(
            f"https://ex.com/{i}" for i in range(15)
        ) + "\n"
        warnings = cloud_agent_runner.daily_signal_limit_warnings("daily/2026-07.md", content)
        self.assertTrue(any("signal sections" in w for w in warnings))
        self.assertTrue(any("public URLs" in w for w in warnings))

    def test_rich_daily_report_within_soft_caps_has_no_warnings(self) -> None:
        # A normal rich daily (14 sections, a 4-URL sources section) is fine now.
        content = "".join(f"#### {i}. Section\n\n- Signal: x\n\n" for i in range(1, 15))
        content += "#### 15. Sources\n\n- Sources: https://a https://b https://c https://d\n"
        self.assertEqual(
            cloud_agent_runner.daily_signal_limit_warnings("daily/2026-07.md", content), []
        )

    def test_replace_section_missing_anchor_appends_new_section(self) -> None:
        # A promote-candidates update used replace_section with an invented,
        # malformed anchor for a NEW agent. Instead of discarding the whole
        # task, a non-report file appends a clean new section.
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        old = "# Watchlist\n\n## Cursor\n\n- existing\n"
        out = cloud_agent_runner.merge_update_content(
            old,
            "replace_section",
            "- What it is: orchestrator\n- Source: https://github.com/ruvnet/ruflo\n",
            anchor="## - **ruvnet/ruflo**",
            allow_append_fallback=True,
        )
        self.assertIn("## ruvnet/ruflo", out)
        self.assertIn("orchestrator", out)
        self.assertIn("- existing", out)  # existing content untouched
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["apply_warnings"])

    def test_replace_section_missing_anchor_stays_strict_for_reports(self) -> None:
        old = "## English\n\n### 1. Intro\n\n- x\n"
        with self.assertRaises(SystemExit):
            cloud_agent_runner.merge_update_content(
                old, "replace_section", "- body", anchor="### 99. Nope", allow_append_fallback=False
            )

    def test_monthly_new_section_is_appended_inside_english_block(self) -> None:
        # Issue #80: the monthly task emitted `replace_section` for a section the
        # month file never had (`### Weekly Coverage`) and the whole task was
        # refused. It must append instead, at its own heading level, and land in
        # the English block rather than after the Chinese one.
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        old = (
            "# Monthly\n\n## English\n\n### 1. Executive Summary\n\n- a\n\n"
            "## 中文\n\n### 1. 摘要\n\n- 甲\n"
        )
        out = cloud_agent_runner.merge_update_content(
            old,
            "replace_section",
            "- W30: https://example.com/w30\n",
            anchor="### Weekly Coverage",
            allow_append_fallback=True,
        )
        self.assertIn("### Weekly Coverage", out)
        self.assertNotIn("\n## Weekly Coverage\n", out)  # level preserved
        self.assertNotIn("\n\n\n", out)
        self.assertLess(out.index("### Weekly Coverage"), out.index("## 中文"))
        self.assertIn("- a", out)
        self.assertIn("- 甲", out)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["apply_warnings"])

    def test_new_section_is_appended_into_the_within_block(self) -> None:
        # The 2026-07-31 monthly emitted `### Weekly Coverage` twice, once per
        # language. Ignoring `within` stacked both copies in the English block.
        old = "# M\n\n## English\n\n### 1. Sum\n\n- a\n\n## 中文\n\n### 1. 摘\n\n- 甲\n"
        first = cloud_agent_runner.merge_update_content(
            old,
            "replace_section",
            "- W30 EN\n",
            anchor="### Weekly Coverage",
            within="## English",
            allow_append_fallback=True,
        )
        out = cloud_agent_runner.merge_update_content(
            first,
            "replace_section",
            "- W30 中文\n",
            anchor="### Weekly Coverage",
            within="## 中文",
            allow_append_fallback=True,
        )
        self.assertEqual(out.count("### Weekly Coverage"), 2)
        self.assertLess(out.index("- W30 EN"), out.index("## 中文"))
        self.assertGreater(out.index("- W30 中文"), out.index("## 中文"))

    def test_within_block_confines_anchor_recovery(self) -> None:
        # A `## 中文` update must never be retargeted onto the mirrored English
        # section — that silently overwrites one language with the other.
        old = "# M\n\n## English\n\n### Weekly Coverage\n\n- EN body\n\n## 中文\n\n### 1. 摘\n\n- 甲\n"
        out = cloud_agent_runner.merge_update_content(
            old,
            "replace_section",
            "- 中文 body\n",
            anchor="### Weekly Coverage",
            within="## 中文",
            allow_append_fallback=True,
        )
        self.assertIn("- EN body", out)
        self.assertGreater(out.index("- 中文 body"), out.index("## 中文"))

    def test_renumbered_anchor_is_recovered_not_appended(self) -> None:
        # A retitled/renumbered anchor is a naming slip: retarget it onto the one
        # heading that matches, instead of appending a duplicate section.
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        old = "# Weekly\n\n## English\n\n### 2. Watchlist Changes\n\n- old body\n"
        out = cloud_agent_runner.merge_update_content(
            old,
            "replace_section",
            "- new body\n",
            anchor="### Watchlist changes",
            allow_append_fallback=True,
        )
        self.assertIn("- new body", out)
        self.assertNotIn("- old body", out)
        self.assertEqual(out.count("Watchlist"), 1)
        self.assertTrue(
            any("recovered" in w for w in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_missing_within_block_is_recovered(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        old = "# Weekly\n\n## English\n\n### 3. Evidence\n\n- old\n"
        out = cloud_agent_runner.merge_update_content(
            old,
            "replace_section",
            "- new\n",
            anchor="### 3. Evidence",
            within="## English Report",
            allow_append_fallback=True,
        )
        self.assertIn("- new", out)
        self.assertNotIn("- old", out)

    def test_recovery_is_skipped_when_disabled(self) -> None:
        old = "# Daily\n\n## 2026-07-01\n\n#### 2. New Signals\n\n- old\n"
        with self.assertRaises(SystemExit):
            cloud_agent_runner.merge_update_content(
                old,
                "replace_section",
                "- new\n",
                anchor="#### 2. New signals",
                allow_append_fallback=False,
                recover_anchor=False,
            )

    def test_existing_anchor_is_still_replaced(self) -> None:
        old = "# Watchlist\n\n## Cursor\n\n- old body\n"
        out = cloud_agent_runner.merge_update_content(
            old, "replace_section", "- new body\n", anchor="## Cursor", allow_append_fallback=True
        )
        self.assertIn("new body", out)
        self.assertNotIn("old body", out)

    def test_prune_removes_empty_shell_but_preserves_filled_days(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir()
            empty = agent_radar.daily_entry(dt.date(2026, 7, 8))
            filled = (
                "## 2026-07-07\n\n### English\n\n#### 1. New Signals\n\n"
                "- Signal: Real thing shipped.\n  - Source: https://example.com/x\n\n"
                "### 中文\n\n#### 1. New Signals\n\n- 信号：真实内容。\n"
            )
            (root / "daily" / "2026-07.md").write_text(
                "# Daily Agent Radar - 2026-07\n\n" + filled + "\n\n---\n\n" + empty,
                encoding="utf-8",
            )
            removed = agent_radar.prune_empty_daily_block(root, dt.date(2026, 7, 8))
            self.assertTrue(removed)
            text = (root / "daily" / "2026-07.md").read_text(encoding="utf-8")
            self.assertNotIn("## 2026-07-08", text)
            self.assertIn("Real thing shipped.", text)
            self.assertIn("## 2026-07-07", text)
            # A second prune of the filled day must NOT remove it.
            self.assertFalse(agent_radar.prune_empty_daily_block(root, dt.date(2026, 7, 7)))


if __name__ == "__main__":
    unittest.main()


class GatewayTokenUsageTest(unittest.TestCase):
    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["token_usage"] = {}

    def test_usage_accumulates_per_model(self) -> None:
        cloud_agent_runner.record_gateway_usage(
            "openai/gpt-5-nano", {"usage": {"prompt_tokens": 1200, "completion_tokens": 300}}
        )
        cloud_agent_runner.record_gateway_usage(
            "openai/gpt-5-nano", {"usage": {"prompt_tokens": 800, "completion_tokens": 100}}
        )
        cloud_agent_runner.record_gateway_usage(
            "openai/gpt-oss-120b", {"usage": {"input_tokens": 5000, "output_tokens": 2000}}
        )
        usage = cloud_agent_runner.RUN_AUDIT["token_usage"]
        self.assertEqual(usage["openai/gpt-5-nano"], {"calls": 2, "input_tokens": 2000, "output_tokens": 400})
        self.assertEqual(usage["openai/gpt-oss-120b"]["input_tokens"], 5000)
        self.assertEqual(cloud_agent_runner.total_gateway_tokens(), (7000, 2400))

    def test_missing_or_empty_usage_is_not_guessed(self) -> None:
        cloud_agent_runner.record_gateway_usage("m", {"choices": []})
        cloud_agent_runner.record_gateway_usage("m", {"usage": {}})
        cloud_agent_runner.record_gateway_usage("m", {"usage": {"prompt_tokens": 0}})
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["token_usage"], {})
        self.assertEqual(cloud_agent_runner.total_gateway_tokens(), (0, 0))

    def test_merge_token_usage_sums_counters(self) -> None:
        dst: dict[str, dict[str, int]] = {}
        cloud_agent_runner.merge_token_usage(
            dst, {"m": {"calls": 1, "input_tokens": 10, "output_tokens": 2}}
        )
        cloud_agent_runner.merge_token_usage(
            dst, {"m": {"calls": 2, "input_tokens": 5, "output_tokens": 1}, "n": {"calls": 1}}
        )
        self.assertEqual(dst["m"], {"calls": 3, "input_tokens": 15, "output_tokens": 3})
        self.assertEqual(dst["n"]["calls"], 1)
        cloud_agent_runner.merge_token_usage(dst, None)
        cloud_agent_runner.merge_token_usage(dst, {"bad": "not-a-dict"})
        self.assertNotIn("bad", dst)

    def test_preflight_screening_tokens_survive_the_task_reset(self) -> None:
        # Shared screening runs before run_task's reset. Its calls were carried
        # over via preflight_screen_calls but its tokens were being discarded —
        # exactly the stage most likely to be on a paid model.
        cloud_agent_runner.RUN_AUDIT["token_usage"] = {}
        cloud_agent_runner.record_gateway_usage(
            "openai/gpt-5-mini", {"usage": {"prompt_tokens": 40000, "completion_tokens": 900}}
        )
        preflight = cloud_agent_runner.merge_token_usage(
            {}, cloud_agent_runner.RUN_AUDIT["token_usage"]
        )
        # what run_task's reset now does
        cloud_agent_runner.RUN_AUDIT["token_usage"] = cloud_agent_runner.merge_token_usage(
            {}, preflight
        )
        cloud_agent_runner.record_gateway_usage(
            "openai/gpt-oss-120b", {"usage": {"prompt_tokens": 26000, "completion_tokens": 6000}}
        )
        self.assertEqual(cloud_agent_runner.total_gateway_tokens(), (66000, 6900))
        self.assertIn("openai/gpt-5-mini", cloud_agent_runner.RUN_AUDIT["token_usage"])


class DirectionGateHolesTest(unittest.TestCase):
    """The direction quotas enforce 方向合理性; all three were inert."""

    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["social_discussion_labeled"] = 0

    def test_prose_words_no_longer_satisfy_the_discussion_gate(self) -> None:
        # "operator" is in every block (the prompt asks each bullet for
        # "So what: ... for an operator"), and "discussion" is in most Lead
        # Analysis paragraphs. Both used to pass this gate on their own.
        prose = (
            "#### 1. Lead Analysis\n\nToday's discussion among operators centred on "
            "agent security; the thread of vendor responses is the storyline.\n\n"
            "#### 2. New Signals\n\n- Signal: OpenAI shipped X.\n"
            "  - Source: https://openai.com/index/x\n"
        )
        self.assertFalse(cloud_agent_runner.content_has_social_discussion_signal(prose))

    def test_cited_discussion_bullet_satisfies_the_gate(self) -> None:
        cited = (
            "#### 2. New Signals\n\n- Signal: HN debates agent sandboxes.\n"
            "  - Source: https://news.ycombinator.com/item?id=1\n"
        )
        self.assertTrue(cloud_agent_runner.content_has_social_discussion_signal(cited))

    def test_missing_x_none_is_not_a_declared_gap(self) -> None:
        # `- Missing social/discussion: none` means nothing was missing. Read as
        # a declared gap it both opened the escape hatch and forced
        # has_discussion to False — two bugs that masked each other.
        text = "#### 8. Assessment & Gaps\n\n- Missing social/discussion: none\n"
        self.assertFalse(cloud_agent_runner.content_has_direction_gap(text, "discussion"))
        real = "#### 8. Assessment & Gaps\n\n- Missing social/discussion: lanes were empty.\n"
        self.assertTrue(cloud_agent_runner.content_has_direction_gap(real, "discussion"))

    def test_bare_word_gap_no_longer_opens_the_escape_hatch(self) -> None:
        # Section 8 is titled "Assessment & Gaps", so `"gap" in text` was true
        # for every block: the mainstream and user hatches were always open.
        text = "#### 8. Assessment & Gaps\n\n- Mainstream vendors looked quiet today.\n"
        self.assertFalse(cloud_agent_runner.content_has_direction_gap(text, "mainstream"))
        self.assertFalse(cloud_agent_runner.content_has_direction_gap(text, "user"))
        named = "#### 8. Assessment & Gaps\n\n- Missing mainstream_product: nothing shipped.\n"
        self.assertTrue(cloud_agent_runner.content_has_direction_gap(named, "mainstream"))


class DiscussionInjectionTest(unittest.TestCase):
    def test_dropped_discussion_candidates_are_auto_added(self) -> None:
        cloud_agent_runner.RUN_AUDIT["discussion_auto_added"] = 0
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "title": "Operators report Claude Code /doctor saves long runs",
                        "why_it_matters": "Field workaround for stalled sessions.",
                        "signal_class": "user_workflow",
                        "relevance_score": 8,
                        "evidence": ["https://www.reddit.com/r/ClaudeAI/comments/abc/x"],
                    }
                ]
            }
        )
        result = {
            "updates": [
                {
                    "path": "daily/2026-08.md",
                    "mode": "append",
                    "content": (
                        "## 2026-08-03\n\n### English\n\n#### 2. New Signals\n\n"
                        "- Signal: OpenAI shipped X.\n  - Source: https://openai.com/index/x\n\n"
                        "### 中文\n\n#### 2. 新信号\n\n- 信号：OpenAI 发布 X。\n"
                    ),
                }
            ]
        }
        injected = cloud_agent_runner.inject_missing_discussion_signals(result, screen)
        self.assertEqual(injected, 1)
        content = result["updates"][0]["content"]
        self.assertIn("#### 4. User Workflow & Field Notes", content)
        self.assertIn("reddit.com/r/ClaudeAI", content)
        self.assertIn("auto-added by the runner", content)
        # English block only — the Chinese block is left to the model.
        self.assertLess(content.index("reddit.com"), content.index("### 中文"))
        # And the repaired block now satisfies the gate it would have failed.
        english = content[: content.index("### 中文")]
        self.assertTrue(cloud_agent_runner.content_has_social_discussion_signal(english))
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["discussion_auto_added"], 1)

    def test_already_covered_candidates_are_not_duplicated(self) -> None:
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "title": "Operators report Claude Code /doctor saves long runs",
                        "evidence": ["https://www.reddit.com/r/ClaudeAI/comments/abc/x"],
                    }
                ]
            }
        )
        result = {
            "updates": [
                {
                    "path": "daily/2026-08.md",
                    "mode": "append",
                    "content": (
                        "## 2026-08-03\n\n### English\n\n#### 4. User Workflow & Field Notes\n\n"
                        "- Signal: Operators report Claude Code /doctor saves long runs\n"
                        "  - Source: https://www.reddit.com/r/ClaudeAI/comments/abc/x\n"
                    ),
                }
            ]
        }
        self.assertEqual(cloud_agent_runner.inject_missing_discussion_signals(result, screen), 0)


class InjectorTargetAgreementTest(unittest.TestCase):
    """Injectors and gates must read the same authoritative field (Issue #93)."""

    SCREEN = json.dumps(
        {
            "candidates": [
                {
                    "title": "Cloudflare: Your agent needs a computer, not a container",
                    "why_it_matters": "Agent runtime shift.",
                    "signal_class": "mainstream_product",
                    "relevance_score": 9,
                    "confidence": "high",
                    "evidence": ["https://blog.cloudflare.com/agent-computer"],
                }
            ]
        }
    )
    DAY = (
        "## 2026-08-04\n\n### English\n\n#### 2. New Signals\n\n"
        "- Signal: Something else.\n  - Source: https://openai.com/x\n\n"
        "#### 8. Assessment & Gaps\n\n- g\n\n"
        "### 中文\n\n#### 2. 新信号\n\n- 信号：别的。\n"
    )

    def _shapes(self) -> dict[str, dict]:
        return {
            "updates+content": {
                "updates": [{"path": "daily/2026-08.md", "mode": "append", "content": self.DAY}]
            },
            "updates+both_blocks": {
                "updates": [
                    {
                        "path": "daily/2026-08.md",
                        "mode": "append",
                        "day_heading": "## 2026-08-04",
                        "english_block": "#### 2. New Signals\n\n- Signal: Something else.\n",
                        "chinese_block": "#### 2. 新信号\n\n- 信号：别的。\n",
                    }
                ]
            },
            # english_block without chinese_block: normalize_result_updates falls
            # back to `content`, so an injector writing english_block was a
            # silent no-op that still reported success.
            "updates+english_block_only": {
                "updates": [
                    {
                        "path": "daily/2026-08.md",
                        "mode": "append",
                        "english_block": "#### 2. New Signals\n\n- Signal: Something else.\n",
                        "content": self.DAY,
                    }
                ]
            },
            # Legacy `files` array: read by the gates, never visited by injectors.
            "files_legacy": {"files": [{"path": "daily/2026-08.md", "content": self.DAY}]},
        }

    def test_mainstream_injection_reaches_the_gate_in_every_shape(self) -> None:
        for name, result in self._shapes().items():
            with self.subTest(shape=name):
                cloud_agent_runner.inject_missing_mainstream_signals(result, self.SCREEN)
                hay = "\n".join(cloud_agent_runner.daily_update_bodies(result)).lower()
                self.assertIn("cloudflare", hay)
                # The gate uses exactly this check; it must now pass.
                cloud_agent_runner.validate_must_cover_mainstream(result, self.SCREEN)

    def test_chinese_block_is_never_touched(self) -> None:
        for name, result in self._shapes().items():
            with self.subTest(shape=name):
                cloud_agent_runner.inject_missing_mainstream_signals(result, self.SCREEN)
                hay = "\n".join(cloud_agent_runner.daily_update_bodies(result))
                self.assertIn("信号：别的", hay)
                self.assertNotIn("Cloudflare", hay.split("### 中文", 1)[-1])

    def test_targets_skip_non_daily_and_malformed_entries(self) -> None:
        result = {
            "updates": [
                {"path": "radar.md", "content": "x"},
                "not-a-dict",
                {"path": "daily/2026-08.md"},
                {"path": "daily/2026-08.md", "content": "   "},
            ],
            "files": [{"path": "weekly/2026-W32.md", "content": "y"}],
        }
        self.assertEqual(cloud_agent_runner.daily_update_block_targets(result), [])


class HonestDiscussionMetricTest(unittest.TestCase):
    def test_model_count_is_captured_before_repair(self) -> None:
        # The 2026-08-03 daily recorded discussion_signal_count=3 with
        # discussion_auto_added=3: the model wrote none. That metric is
        # measured after the injector, so it cannot stand alone as the
        # honest measure of model output.
        day = (
            "## 2026-08-04\n\n### English\n\n#### 2. New Signals\n\n"
            "- Signal: Vendor shipped X.\n  - Source: https://openai.com/x\n\n"
            "### 中文\n\n#### 2. 新信号\n\n- 信号：厂商发布 X。\n"
        )
        result = {"updates": [{"path": "daily/2026-08.md", "mode": "append", "content": day}]}
        self.assertEqual(cloud_agent_runner.count_discussion_signal_bullets(result), 0)
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "title": "Operators debate agent sandboxes on Bluesky",
                        "evidence": ["https://bsky.app/profile/a/post/1"],
                    }
                ]
            }
        )
        cloud_agent_runner.inject_missing_discussion_signals(result, screen)
        # Post-repair the count is 1, which is exactly why the pre-repair
        # number has to be recorded separately.
        self.assertEqual(cloud_agent_runner.count_discussion_signal_bullets(result), 1)

    def test_model_written_discussion_bullets_are_counted(self) -> None:
        day = (
            "## 2026-08-04\n\n### English\n\n#### 2. New Signals\n\n"
            "- Signal: HN debates agent sandboxes.\n"
            "  - Source: https://news.ycombinator.com/item?id=1\n\n"
            "### 中文\n\n#### 2. 新信号\n\n- 信号：HN 讨论。\n"
        )
        result = {"updates": [{"path": "daily/2026-08.md", "mode": "append", "content": day}]}
        self.assertEqual(cloud_agent_runner.count_discussion_signal_bullets(result), 1)


class PoolSizeIndependentRecallTest(unittest.TestCase):
    """Recall must measure model effort, not pool size (Issue #96)."""

    @staticmethod
    def _screen(n: int) -> str:
        return json.dumps(
            {
                "candidates": [
                    {
                        "title": f"Vendor {i} shipped thing {i}",
                        "signal_class": "mainstream_product",
                        "confidence": "high" if i < 5 else "medium",
                        "relevance_score": 9 - (i % 5),
                        "evidence": [f"https://vendor{i}.com/post"],
                    }
                    for i in range(n)
                ]
            }
        )

    @staticmethod
    def _result(covered: int) -> dict:
        cited = " ".join(f"https://vendor{i}.com/post" for i in range(covered))
        return {
            "updates": [
                {
                    "path": "daily/2026-08.md",
                    "mode": "append",
                    "content": (
                        "## 2026-08-20\n\n### English\n\n#### 2. New Signals\n\n"
                        f"- Signal: covered {cited}\n"
                    ),
                }
            ]
        }

    def test_same_coverage_scores_the_same_regardless_of_pool_size(self) -> None:
        # Restoring 4 shards in v0.22.1 grew the pool ~16 -> ~50, and the old
        # whole-pool denominator voided four August dailies on days the
        # pipeline was working better.
        small = cloud_agent_runner.compute_synthesis_recall_details(
            self._screen(12), self._result(7)
        )["weighted_recall"]
        large = cloud_agent_runner.compute_synthesis_recall_details(
            self._screen(50), self._result(7)
        )["weighted_recall"]
        self.assertGreaterEqual(
            large, cloud_agent_runner.DEFAULT_MIN_WEIGHTED_SYNTHESIS_RECALL
        )
        # A 4x pool must not cost more than the shown-list cap explains.
        self.assertGreater(large, 7 / 50)
        self.assertGreaterEqual(small, large)

    def test_ignoring_screening_still_fails(self) -> None:
        details = cloud_agent_runner.compute_synthesis_recall_details(
            self._screen(50), self._result(0)
        )
        self.assertLess(
            details["weighted_recall"],
            cloud_agent_runner.DEFAULT_MIN_WEIGHTED_SYNTHESIS_RECALL,
        )


class DailySectionRepairTest(unittest.TestCase):
    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        cloud_agent_runner.RUN_AUDIT["daily_sections_repaired"] = 0

    def _result(self, english: str) -> dict:
        return {
            "updates": [
                {
                    "path": "daily/2026-08.md",
                    "mode": "append",
                    "content": f"## 2026-08-20\n\n### English\n\n{english}",
                }
            ]
        }

    def test_missing_required_sections_are_added_not_refused(self) -> None:
        result = self._result(
            "#### 1. Lead Analysis\n\nnarrative\n\n#### 2. New Signals\n\n- Signal: x\n"
        )
        healed = cloud_agent_runner.ensure_daily_required_sections(result)
        self.assertIn("#### 6. Storage / Infra Angle", healed)
        # The gate that used to void the daily now passes.
        cloud_agent_runner.validate_daily_section_structure(result)
        body = result["updates"][0]["content"]
        self.assertIn("Missing storage/infra angle", body)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["apply_warnings"])

    def test_block_without_lead_or_signals_still_refuses(self) -> None:
        result = self._result("#### 3. Mainstream Agent Progress\n\n- x\n")
        with self.assertRaises(SystemExit):
            cloud_agent_runner.ensure_daily_required_sections(result)

    def test_radar_sweep_lands_without_a_section_8_anchor(self) -> None:
        cloud_agent_runner.SHARED_SWEEP_LINES[:] = ["- [infra] thing | https://x.dev/a"]
        try:
            result = self._result("#### 2. New Signals\n\n- Signal: x\n")
            cloud_agent_runner.inject_deterministic_radar_sweep(result)
            self.assertIn("#### 7. Radar Sweep", result["updates"][0]["content"])
        finally:
            cloud_agent_runner.SHARED_SWEEP_LINES[:] = []


class ChineseMirrorRepairTest(unittest.TestCase):
    """Weekly/monthly 中文 gate: repair or degrade, never discard (Issue #96)."""

    def _thin_monthly(self) -> str:
        english = "\n".join(
            f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
            for i in range(1, 26)
        )
        return (
            "# Agent Radar Monthly - 2026-08\n\n## English\n\n"
            f"### 1. Executive Summary\n\n{english}\n\n"
            "## 中文\n\n### 1. Executive Summary\n\n- 摘要：\n"
        )

    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["chinese_mirror_repaired"] = 0
        cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"] = 0
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []

    def test_thin_chinese_is_the_precondition(self) -> None:
        self.assertTrue(radar_bilingual.missing_chinese_substance(self._thin_monthly()))

    def test_mirror_regeneration_repairs_the_report(self) -> None:
        chinese = "\n".join(
            f"- 信号 {i}：某厂商发布了一项真实进展。https://example.com/{i}" for i in range(1, 26)
        )
        with mock.patch.object(
            cloud_agent_runner,
            "request_chinese_mirror",
            return_value=f"### 1. Executive Summary\n\n{chinese}",
        ):
            out = cloud_agent_runner.repair_report_chinese_block(
                "monthly/2026-08.md", self._thin_monthly()
            )
        self.assertFalse(radar_bilingual.missing_chinese_substance(out))
        self.assertIn("Signal 25", out)  # English body preserved verbatim
        self.assertIn("信号 25", out)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["chinese_mirror_repaired"], 1)

    def test_failed_mirror_publishes_labeled_instead_of_raising(self) -> None:
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=""):
            out = cloud_agent_runner.repair_report_chinese_block(
                "monthly/2026-08.md", self._thin_monthly()
            )
        self.assertIn("Signal 25", out)
        self.assertIn("本期中文镜像未能生成", out)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"], 1)
        # The label must NOT flip the metric: a degraded report still reports
        # as thin, otherwise the repair would be dressing up the measurement.
        self.assertTrue(radar_bilingual.missing_chinese_substance(out))

    def test_apply_updates_no_longer_discards_a_thin_weekly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "weekly").mkdir()
            target = root / "weekly" / "2026-W34.md"
            target.write_text(
                "# Agent Radar Weekly - 2026-W34\n\n## English\n\n### 1. Summary\n\n- old\n\n"
                "## 中文\n\n### 1. Summary\n\n- 摘要：\n",
                encoding="utf-8",
            )
            english = "\n".join(
                f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
                for i in range(1, 26)
            )
            with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=""):
                changed = cloud_agent_runner.apply_updates(
                    root,
                    ["weekly/2026-W34.md"],
                    {
                        "updates": [
                            {
                                "path": "weekly/2026-W34.md",
                                "mode": "replace_section",
                                "anchor": "### 1. Summary",
                                "within": "## English",
                                "content": english,
                            }
                        ]
                    },
                )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertIn("Signal 25", text)  # would have been discarded before
            self.assertEqual(cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"], 1)

    def test_daily_block_format_still_refuses(self) -> None:
        # Only the block-bilingual weekly/monthly path is regenerated; the
        # daily's own gate has not been failing and keeps its behavior.
        daily = (
            "## 2026-08-20\n\n### English\n\n"
            + "\n".join(f"#### {i}. Section\n\n- Signal: x https://e.com/{i}\n" for i in range(1, 6))
            + "\n### 中文\n\n#### 1. 章节\n\n- 空：\n"
        )
        self.assertFalse(radar_bilingual.is_block_bilingual_format(daily))


class ChineseMirrorDiagnosticsTest(unittest.TestCase):
    """The 2026-08-20 weekly degraded twice and the log could not say why."""

    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        cloud_agent_runner.RUN_AUDIT["chinese_mirror_repaired"] = 0
        cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"] = 0

    def _monthly(self) -> str:
        english = "\n".join(
            f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
            for i in range(1, 26)
        )
        return (
            "# Agent Radar Monthly - 2026-08\n\n## English\n\n"
            f"### 1. Executive Summary\n\n{english}\n\n"
            "## 中文\n\n### 1. Executive Summary\n\n- 摘要：\n"
        )

    def test_missing_chinese_block_key_is_named(self) -> None:
        with mock.patch.object(
            cloud_agent_runner,
            "call_ai_gateway_model",
            return_value={"choices": [{"message": {"content": '{"chinese": "x"}'}}]},
        ), mock.patch.object(cloud_agent_runner, "model_provider", return_value="vercel-ai-gateway"):
            self.assertEqual(cloud_agent_runner.request_chinese_mirror("weekly/x.md", "body"), "")
        joined = "\n".join(cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        self.assertIn("no `chinese_block`", joined)
        self.assertIn("chinese", joined)  # the keys that WERE present

    def test_thin_mirror_records_the_shortfall(self) -> None:
        with mock.patch.object(
            cloud_agent_runner, "request_chinese_mirror", return_value="### 1. 摘要\n\n- 一条。"
        ):
            cloud_agent_runner.repair_report_chinese_block("monthly/2026-08.md", self._monthly())
        joined = "\n".join(cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        self.assertIn("CJK line(s), need", joined)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"], 1)


class ChineseSubstanceInvariantTest(unittest.TestCase):
    """`--require-chinese` is a repo invariant on push/PR; a RECORDED
    degradation is an accepted state, an unmarked one is not (Issue #96)."""

    def _thin(self, marker: bool) -> str:
        english = "\n".join(
            f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
            for i in range(1, 26)
        )
        note = (
            f"> {radar_bilingual.CHINESE_MIRROR_DEGRADED_MARKER}，请以上方 `## English` 正文为准。\n\n"
            if marker
            else ""
        )
        return (
            "# Agent Radar Weekly - 2026-W34\n\n## English\n\n"
            f"### 1. Summary\n\n{english}\n\n## 中文\n\n{note}### 1. Summary\n\n- 摘要：\n"
        )

    def _findings(self, marker: bool) -> tuple[list[str], list[str]]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "2026-W34.md"
            path.write_text(self._thin(marker), encoding="utf-8")
            return agent_radar.chinese_substance_findings(path, strict=True)

    def test_unmarked_thin_report_is_still_an_error(self) -> None:
        errors, warnings = self._findings(marker=False)
        self.assertEqual(len(errors), 1)
        self.assertEqual(warnings, [])

    def test_recorded_degradation_is_a_warning_not_an_error(self) -> None:
        errors, warnings = self._findings(marker=True)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("recorded as a mirror degradation", warnings[0])

    def test_runner_marker_matches_what_validate_looks_for(self) -> None:
        # The runner writes the note and validate detects it; a drift between
        # the two would silently turn every degraded report into a CI failure.
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"] = 0
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=""):
            out = cloud_agent_runner.repair_report_chinese_block(
                "weekly/2026-W34.md", self._thin(marker=False)
            )
        self.assertTrue(radar_bilingual.has_recorded_chinese_degradation(out))


class ChineseMirrorPromptTest(unittest.TestCase):
    """The 2026-08-21 monthly logged `regenerated 0 CJK line(s), need 17`.

    Only one mirror shape scores zero: Chinese prose with no `- ` bullets —
    and the prompt was asking for exactly that ("Write natural Simplified
    Chinese prose"), while never naming the count the checker required.
    """

    def test_prose_without_bullets_is_the_zero_case(self) -> None:
        prefix = "# Agent Radar Monthly - 2026-08"
        english = "\n".join(f"- Signal {i}: vendor shipped X. https://e.com/{i}" for i in range(1, 28))
        bullets = "\n".join(f"- 信号 {i}：厂商发布了 X。" for i in range(1, 20))
        prose = "本月主线是 agent 运行时从容器转向完整计算机，厂商在安全与遏制上投入显著增加。"
        for label, mirror, expect_zero in (
            ("bullets", bullets, False),
            ("bullets under a heading", f"### 1. Summary\n\n{bullets}", False),
            ("prose", prose, True),
        ):
            with self.subTest(shape=label):
                candidate = f"{prefix}\n\n## English\n\n{english}\n\n## 中文\n\n{mirror}\n"
                counted = radar_bilingual.substantive_chinese_cjk_lines(candidate)
                self.assertEqual(counted == 0, expect_zero)

    def test_prompt_demands_bullets_and_names_the_count(self) -> None:
        prompt = cloud_agent_runner.build_chinese_mirror_prompt("monthly/2026-08.md", "- a\n- b\n", 17)
        self.assertIn("markdown bullet starting with `- `", prompt)
        self.assertIn("at least 17", prompt)
        self.assertNotIn("Simplified Chinese prose", prompt)  # the instruction that caused it

    def test_required_count_is_derived_from_the_merged_report(self) -> None:
        english = "\n".join(f"- Signal {i}: x https://e.com/{i}" for i in range(1, 28))
        merged = (
            "# Agent Radar Monthly - 2026-08\n\n## English\n\n"
            f"### 1. Summary\n\n{english}\n\n## 中文\n\n### 1. Summary\n\n- 摘要：\n"
        )
        seen: dict[str, int] = {}

        def _capture(rel_path: str, body: str, required_lines: int = 0) -> str:
            seen["required"] = required_lines
            return ""

        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        cloud_agent_runner.RUN_AUDIT["chinese_mirror_degraded"] = 0
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", _capture):
            cloud_agent_runner.repair_report_chinese_block("monthly/2026-08.md", merged)
        self.assertEqual(
            seen["required"],
            radar_bilingual.required_chinese_lines(radar_bilingual.substantive_english_lines(merged)),
        )
        self.assertGreater(seen["required"], 0)


class StaleDegradationMarkerTest(unittest.TestCase):
    """The 2026-08-21 monthly passed the substance check but still carried the
    marker: a later update supplied the Chinese an earlier mirror could not."""

    def _report(self, chinese_lines: int, marker: bool) -> str:
        english = "\n".join(
            f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
            for i in range(1, 38)
        )
        chinese = "\n".join(f"- 信号 {i}：某厂商发布了一项真实进展。" for i in range(1, chinese_lines + 1))
        note = (
            f"> {radar_bilingual.CHINESE_MIRROR_DEGRADED_MARKER}，请以上方 `## English` 正文为准。\n\n"
            if marker
            else ""
        )
        return (
            "# Agent Radar Monthly - 2026-08\n\n## English\n\n"
            f"### 1. Summary\n\n{english}\n\n## 中文\n\n{note}### 1. Summary\n\n{chinese}\n"
        )

    def test_stripping_keeps_the_chinese_and_drops_only_the_note(self) -> None:
        content = self._report(chinese_lines=28, marker=True)
        self.assertFalse(radar_bilingual.missing_chinese_substance(content))
        out = radar_bilingual.strip_chinese_degradation_note(content)
        self.assertFalse(radar_bilingual.has_recorded_chinese_degradation(out))
        self.assertFalse(radar_bilingual.missing_chinese_substance(out))
        self.assertIn("信号 28", out)
        self.assertNotIn("\n\n\n", out)

    def test_apply_updates_clears_the_stale_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "monthly").mkdir()
            target = root / "monthly" / "2026-08.md"
            target.write_text(self._report(chinese_lines=28, marker=True), encoding="utf-8")
            cloud_agent_runner.RUN_AUDIT["chinese_mirror_marker_cleared"] = 0
            cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
            changed = cloud_agent_runner.apply_updates(
                root,
                ["monthly/2026-08.md"],
                {
                    "updates": [
                        {
                            "path": "monthly/2026-08.md",
                            "mode": "replace_section",
                            "anchor": "### 1. Summary",
                            "within": "## English",
                            "content": "\n".join(
                                f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
                                for i in range(1, 38)
                            ),
                        }
                    ]
                },
            )
            self.assertEqual(changed, 1)
            text = target.read_text(encoding="utf-8")
            self.assertFalse(radar_bilingual.has_recorded_chinese_degradation(text))
            self.assertEqual(cloud_agent_runner.RUN_AUDIT["chinese_mirror_marker_cleared"], 1)

    def test_marker_stays_when_the_report_is_still_thin(self) -> None:
        content = self._report(chinese_lines=3, marker=True)
        self.assertTrue(radar_bilingual.missing_chinese_substance(content))
        # A genuinely thin report keeps its marker; only the stale case clears.
        self.assertTrue(radar_bilingual.has_recorded_chinese_degradation(content))


class DegradationMarkerFloorTest(unittest.TestCase):
    """v0.24.4 cleared the marker whenever `missing_chinese_substance()` said
    False — but that function exempts reports under 10 substantive English
    lines outright, so it says False for a report with NO Chinese at all."""

    def _report(self, english_lines: int, chinese_lines: int) -> str:
        english = "\n".join(
            f"- Signal {i}: a vendor shipped something real. https://example.com/{i}"
            for i in range(1, english_lines + 1)
        )
        chinese = (
            "\n".join(f"- 信号 {i}：某厂商发布了一项真实进展。" for i in range(1, chinese_lines + 1))
            or "- 摘要："
        )
        note = f"> {radar_bilingual.CHINESE_MIRROR_DEGRADED_MARKER}，请以上方 `## English` 正文为准。\n\n"
        return (
            "# Agent Radar Weekly - 2026-W34\n\n## English\n\n"
            f"### 1. Summary\n\n{english}\n\n## 中文\n\n{note}### 1. Summary\n\n{chinese}\n"
        )

    def test_low_volume_exemption_does_not_clear_the_marker(self) -> None:
        # English shrinks below 10 lines with the Chinese half still empty:
        # the publish gate exempts it, but the marker is still accurate.
        content = self._report(english_lines=5, chinese_lines=0)
        self.assertFalse(radar_bilingual.missing_chinese_substance(content))
        self.assertFalse(radar_bilingual.chinese_half_clears_floor(content))

    def test_genuinely_mirrored_report_clears(self) -> None:
        content = self._report(english_lines=37, chinese_lines=28)
        self.assertTrue(radar_bilingual.chinese_half_clears_floor(content))

    def test_thin_chinese_does_not_clear(self) -> None:
        content = self._report(english_lines=37, chinese_lines=3)
        self.assertFalse(radar_bilingual.chinese_half_clears_floor(content))

    def test_apply_updates_keeps_the_marker_under_the_exemption(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "weekly").mkdir()
            target = root / "weekly" / "2026-W34.md"
            target.write_text(self._report(english_lines=37, chinese_lines=0), encoding="utf-8")
            cloud_agent_runner.RUN_AUDIT["chinese_mirror_marker_cleared"] = 0
            cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
            with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=""):
                cloud_agent_runner.apply_updates(
                    root,
                    ["weekly/2026-W34.md"],
                    {
                        "updates": [
                            {
                                "path": "weekly/2026-W34.md",
                                "mode": "replace_section",
                                "anchor": "### 1. Summary",
                                "within": "## English",
                                "content": "\n".join(
                                    f"- Signal {i}: a vendor shipped something real."
                                    f" https://example.com/{i}"
                                    for i in range(1, 6)
                                ),
                            }
                        ]
                    },
                )
            text = target.read_text(encoding="utf-8")
            self.assertTrue(radar_bilingual.has_recorded_chinese_degradation(text))
            self.assertEqual(cloud_agent_runner.RUN_AUDIT["chinese_mirror_marker_cleared"], 0)
