from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import time
import unittest
import datetime as dt
import urllib.request
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "cloud_agent_runner.py"
STATE_PATH = REPO_ROOT / "scripts" / "radar_collector_state.py"


spec = importlib.util.spec_from_file_location("cloud_agent_runner", MODULE_PATH)
assert spec is not None
cloud_agent_runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cloud_agent_runner)

state_spec = importlib.util.spec_from_file_location("radar_collector_state", STATE_PATH)
assert state_spec is not None
radar_collector_state = importlib.util.module_from_spec(state_spec)
assert state_spec.loader is not None
state_spec.loader.exec_module(radar_collector_state)


class CloudAgentRunnerTest(unittest.TestCase):
    def test_openrouter_default_model_route_is_small(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                cloud_agent_runner.openrouter_models_for_task("daily"),
                ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
            )
            self.assertEqual(
                cloud_agent_runner.openrouter_models_for_task("source-sweep"),
                ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
            )
            self.assertEqual(
                cloud_agent_runner.openrouter_models_for_task("weekly"),
                ["deepseek/deepseek-v4-flash", "z-ai/glm-5.2"],
            )
            self.assertEqual(
                cloud_agent_runner.openrouter_models_for_task("monthly"),
                ["deepseek/deepseek-v4-flash", "z-ai/glm-5.2"],
            )
            self.assertEqual(
                cloud_agent_runner.openrouter_models_for_task("promote-candidates"),
                ["deepseek/deepseek-v4-pro"],
            )

    def test_auto_tasks_include_candidate_promotion_on_sunday(self) -> None:
        tasks = cloud_agent_runner.auto_tasks(cloud_agent_runner.parse_date("2026-07-05"))
        self.assertIn("daily", tasks)
        self.assertIn("source-sweep", tasks)
        self.assertIn("weekly", tasks)
        self.assertIn("promote-candidates", tasks)

    def test_auto_tasks_promote_twice_a_week(self) -> None:
        tasks = cloud_agent_runner.auto_tasks(cloud_agent_runner.parse_date("2026-07-01"))
        self.assertIn("daily", tasks)
        self.assertIn("source-sweep", tasks)
        self.assertIn("promote-candidates", tasks)
        self.assertNotIn("weekly", tasks)

    def test_daily_can_update_source_registry(self) -> None:
        self.assertIn("sources.md", cloud_agent_runner.TASK_CONFIG["daily"]["allowed"])

    def test_public_source_collection_can_be_disabled(self) -> None:
        with mock.patch.dict(os.environ, {"PUBLIC_SOURCE_COLLECTION": "false"}, clear=True):
            self.assertIn("disabled", cloud_agent_runner.collect_public_sources("daily"))

    def test_reddit_search_disabled_by_default(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(cloud_agent_runner.collector_enabled("reddit"))
            self.assertTrue(cloud_agent_runner.collector_enabled("reddit-rss"))
            self.assertTrue(cloud_agent_runner.collector_enabled("bluesky"))

    def test_reddit_search_can_be_enabled(self) -> None:
        with mock.patch.dict(os.environ, {"COLLECT_REDDIT": "true"}, clear=True):
            self.assertTrue(cloud_agent_runner.collector_enabled("reddit"))

    def test_x_requires_bearer_token(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(cloud_agent_runner.collector_enabled("x"))
        with mock.patch.dict(os.environ, {"X_BEARER_TOKEN": "token"}, clear=True):
            self.assertTrue(cloud_agent_runner.collector_enabled("x"))

    def test_bluesky_collector_parses_posts(self) -> None:
        payload = {
            "posts": [
                {
                    "uri": "at://did:plc:abc/app.bsky.feed.post/3jz7",
                    "indexedAt": "2026-07-02T00:00:00.000Z",
                    "author": {"handle": "example.bsky.social"},
                    "record": {"text": "AI agent memory update"},
                }
            ]
        }
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        with mock.patch.object(cloud_agent_runner, "request_json", return_value=payload):
            cloud_agent_runner.collect_bluesky_items("AI agent", 1, items, seen)
        self.assertEqual(len(items), 1)
        self.assertIn("bsky.app/profile/example.bsky.social/post/3jz7", items[0]["url"])

    def test_reddit_rss_uses_feed_collector(self) -> None:
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        with mock.patch.object(cloud_agent_runner, "collect_feed_items") as feed_mock:
            cloud_agent_runner.collect_reddit_rss_items("LocalLLaMA", 3, items, seen)
        feed_mock.assert_called_once()
        self.assertIn("reddit.com/r/LocalLLaMA/new.rss", feed_mock.call_args.args[0])

    def test_public_source_budget_is_more_aggressive(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(cloud_agent_runner.public_source_budget("daily"), 50)
            self.assertEqual(cloud_agent_runner.public_source_budget("source-sweep"), 120)
            self.assertEqual(cloud_agent_runner.public_source_budget("weekly"), 120)
            self.assertEqual(cloud_agent_runner.public_source_budget("monthly"), 160)
            self.assertGreaterEqual(cloud_agent_runner.MAX_PUBLIC_SOURCE_ITEMS, 200)

    def test_build_prompt_uses_screening_pass_instead_of_raw_sources(self) -> None:
        prompt = cloud_agent_runner.build_prompt(
            "daily",
            cloud_agent_runner.parse_date("2026-07-02"),
            ["research-log.md"],
            "repo context",
            screened_summary='{"summary":"screened"}',
        )
        self.assertIn("Screening pass", prompt)
        self.assertNotIn("Public source snapshot:", prompt)

    def test_build_prompt_prefers_patch_updates_schema(self) -> None:
        prompt = cloud_agent_runner.build_prompt(
            "daily",
            cloud_agent_runner.parse_date("2026-07-02"),
            ["research-log.md"],
            "repo context",
            public_sources="public source snapshot",
        )
        self.assertIn("prompts/runner-rules.md", prompt)
        rules = (REPO_ROOT / "prompts" / "runner-rules.md").read_text(encoding="utf-8")
        self.assertIn('"mode": "append"', rules)
        self.assertIn("Daily append example", rules)

    def test_runner_rules_bans_paid_search_and_documents_append(self) -> None:
        rules = (REPO_ROOT / "prompts" / "runner-rules.md").read_text(encoding="utf-8")
        self.assertIn("do not use paid search tools", rules)
        self.assertIn("do not rewrite the entire monthly daily file", rules.lower())

    def test_source_queries_cover_social_and_infra_lanes(self) -> None:
        queries = cloud_agent_runner.source_queries_for_task("source-sweep")
        self.assertIn("AI coding agent", queries["reddit"])
        self.assertIn("agent eval framework", queries["github"])
        self.assertIn("browser agent", queries["hn"])
        self.assertIn("mcp server", queries["packages"])

    def test_source_scoring_and_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            item = {
                "source": "github",
                "title": "Agent memory MCP sandbox",
                "url": "https://github.com/example/agent-memory",
                "note": "stars=1200; updated=2026-07-02",
            }
            score = cloud_agent_runner.score_source_item(item, {})
            self.assertGreater(score, 40)
            item["score"] = str(score)
            cloud_agent_runner.update_source_cache(root, [item], cloud_agent_runner.parse_date("2026-07-02"))
            cache_text = (root / "automation" / "source-cache.jsonl").read_text(encoding="utf-8")
            self.assertIn("agent-memory", cache_text)
            cache = cloud_agent_runner.load_source_cache(root)
            self.assertIn(item["url"], cache)

    def test_extracts_github_repos_for_release_tracking(self) -> None:
        repos = cloud_agent_runner.extract_github_repos(
            "See https://github.com/modelcontextprotocol/servers and https://github.com/openai/codex/releases",
            10,
        )
        self.assertIn("modelcontextprotocol/servers", repos)
        self.assertIn("openai/codex", repos)

    def test_release_and_changelog_defaults_are_present(self) -> None:
        self.assertIn("openai/codex", cloud_agent_runner.DEFAULT_RELEASE_REPOS)
        feed_names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_FEEDS]
        self.assertIn("github-changelog", feed_names)
        page_names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_PAGES]
        self.assertIn("cursor-changelog", page_names)
        self.assertIn("anthropic-news", page_names)
        with mock.patch.dict(os.environ, {"MAX_RELEASE_REPOS": "3"}, clear=True):
            repos = cloud_agent_runner.release_repos_from_context(REPO_ROOT, 3)
        self.assertLessEqual(len(repos), 3)

    def test_openrouter_prompt_bans_paid_search_tools(self) -> None:
        rules = (REPO_ROOT / "prompts" / "runner-rules.md").read_text(encoding="utf-8")
        self.assertIn("do not use paid search tools", rules)

        prompt = cloud_agent_runner.build_prompt(
            "daily",
            cloud_agent_runner.parse_date("2026-07-02"),
            ["research-log.md"],
            "repo context",
            "public source snapshot",
        )
        self.assertIn("prompts/runner-rules.md", prompt)
        self.assertIn("Public source snapshot:", prompt)

    def test_source_sweep_is_discovery_only(self) -> None:
        allowed = cloud_agent_runner.TASK_CONFIG["source-sweep"]["allowed"]
        self.assertEqual(allowed, ["sources.md", "research-log.md"])

        prompt = cloud_agent_runner.build_prompt(
            "source-sweep",
            cloud_agent_runner.parse_date("2026-07-02"),
            ["sources.md", "research-log.md"],
            "repo context",
            "public source snapshot",
        )
        rules = (REPO_ROOT / "prompts" / "runner-rules.md").read_text(encoding="utf-8")
        self.assertIn("Source-sweep task gate", rules)
        self.assertIn("Apply the **Source-sweep task gate**", prompt)
        self.assertIn("discovery, not promotion", rules)

    def test_promote_candidates_gate_is_automatic_and_bounded(self) -> None:
        allowed = cloud_agent_runner.TASK_CONFIG["promote-candidates"]["allowed"]
        self.assertIn("agent-watchlist.md", allowed)
        self.assertIn("research-log.md", allowed)

        prompt = cloud_agent_runner.build_prompt(
            "promote-candidates",
            cloud_agent_runner.parse_date("2026-07-05"),
            allowed,
            "repo context",
            "",
        )
        rules = (REPO_ROOT / "prompts" / "runner-rules.md").read_text(encoding="utf-8")
        self.assertIn("Promote-candidates task gate", rules)
        self.assertIn("Apply the **Promote-candidates task gate**", prompt)
        self.assertIn("Promote at most 3 candidates per run.", rules)

    def test_zero_openrouter_budget_dry_runs(self) -> None:
        with mock.patch.dict(os.environ, {"MAX_OPENROUTER_CALLS_PER_TASK": "0"}, clear=True):
            data = cloud_agent_runner.call_openrouter("daily", "prompt", "sources")
        text = cloud_agent_runner.response_output_text(data)
        self.assertIn("OpenRouter call budget is zero", text)

    def test_pypi_updates_collector_parses_rss(self) -> None:
        rss = """<?xml version="1.0"?>
<rss><channel>
<item><title>mcp 1.2.3</title><link>https://pypi.org/project/mcp/</link><description>Model Context Protocol</description></item>
<item><title>other 0.1.0</title><link>https://pypi.org/project/other/</link><description>unrelated</description></item>
</channel></rss>"""
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        with mock.patch.object(urllib.request, "urlopen") as urlopen_mock:
            response = mock.MagicMock()
            response.read.return_value = rss.encode("utf-8")
            response.__enter__.return_value = response
            response.__exit__.return_value = None
            urlopen_mock.return_value = response
            cloud_agent_runner.collect_pypi_updates("mcp", 5, items, seen)
        self.assertEqual(len(items), 1)
        self.assertIn("pypi.org/project/mcp", items[0]["url"])

    def test_reddit_subreddit_rotation_batches_by_day(self) -> None:
        subs = ["a", "b", "c", "d", "e"]
        with mock.patch.object(cloud_agent_runner, "reddit_subreddits", return_value=subs):
            with mock.patch.dict(os.environ, {"REDDIT_RSS_BATCH_SIZE": "2"}, clear=True):
                day_one = cloud_agent_runner.reddit_subreddits_for_day(cloud_agent_runner.parse_date("2026-07-01"))
                day_two = cloud_agent_runner.reddit_subreddits_for_day(cloud_agent_runner.parse_date("2026-07-02"))
        self.assertEqual(len(day_one), 2)
        self.assertEqual(len(day_two), 2)
        self.assertNotEqual(day_one, day_two)

    def test_reddit_rss_default_batch_size_is_one(self) -> None:
        subs = ["a", "b", "c"]
        with mock.patch.object(cloud_agent_runner, "reddit_subreddits", return_value=subs):
            with mock.patch.dict(os.environ, {}, clear=True):
                selected = cloud_agent_runner.reddit_subreddits_for_day(cloud_agent_runner.parse_date("2026-07-02"))
        self.assertEqual(len(selected), 1)

    def test_pypi_enabled_by_default(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertTrue(cloud_agent_runner.collector_enabled("pypi"))

    def test_collect_only_refreshes_health_files(self) -> None:
        def fake_collect(_task: str, _root: Path, _day: cloud_agent_runner.dt.date) -> str:
            cloud_agent_runner.RUN_AUDIT["source_status"] = [
                {"name": "feed:test", "status": "ok", "detail": ""},
            ]
            cloud_agent_runner.RUN_AUDIT["source_lanes"] = {
                "feed": {"ok": 1, "error": 0, "items": 3},
            }
            return "snapshot"

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "radar.md").write_text("# radar\n", encoding="utf-8")
            (root / "agent-watchlist.md").write_text("# watchlist\n", encoding="utf-8")
            with mock.patch.object(cloud_agent_runner, "collect_public_sources", side_effect=fake_collect):
                cloud_agent_runner.run_collect_only(root, "source-sweep", cloud_agent_runner.parse_date("2026-07-02"))
            self.assertTrue((root / "automation" / "source-health.md").exists())
            self.assertTrue((root / "automation" / "source-lanes.md").exists())
            self.assertIn("source-refresh", (root / "automation" / "telemetry" / "2026-07.jsonl").read_text())

    def test_rejected_repo_is_skipped_from_release_tracking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            radar_collector_state.record_repo_rejection(root, "dead/project", "HTTP Error 404: Not Found")
            (root / "sources.md").write_text(
                "https://github.com/dead/project\n",
                encoding="utf-8",
            )
            with mock.patch.object(cloud_agent_runner, "github_repo_exists", return_value=True):
                repos = cloud_agent_runner.release_repos_from_context(root, 5)
            self.assertNotIn("dead/project", repos)

    def test_run_log_and_source_health_are_written_by_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cloud_agent_runner.RUN_AUDIT["provider"] = "openrouter"
            cloud_agent_runner.RUN_AUDIT["models"] = ["deepseek/deepseek-v4-pro"]
            cloud_agent_runner.RUN_AUDIT["openrouter_calls"] = 1
            cloud_agent_runner.RUN_AUDIT["public_source_items"] = 3
            cloud_agent_runner.RUN_AUDIT["collected_source_items"] = 5
            cloud_agent_runner.RUN_AUDIT["source_errors"] = ["feed:test: 404"]
            cloud_agent_runner.RUN_AUDIT["source_status"] = [{"name": "feed:test", "status": "error", "detail": "404"}]
            cloud_agent_runner.RUN_AUDIT["source_lanes"] = {"feed": {"ok": 0, "error": 1, "items": 0}}
            cloud_agent_runner.RUN_AUDIT["budget_status"] = "normal"
            cloud_agent_runner.RUN_AUDIT["started_at"] = 1.0
            day = cloud_agent_runner.parse_date("2026-07-02")
            cloud_agent_runner.append_run_log(root, "source-sweep", day, 2, "summary", ["source"])
            cloud_agent_runner.append_telemetry(root, "source-sweep", day, 2, "summary", ["source"])
            cloud_agent_runner.update_source_health(root, day)
            cloud_agent_runner.update_source_lanes(root, day)

            self.assertIn("OpenRouter calls attempted: 1", (root / "automation" / "runs" / "2026-07.md").read_text())
            self.assertIn("Collected source items before trim: 5", (root / "automation" / "runs" / "2026-07.md").read_text())
            self.assertIn("\"source_error_count\": 1", (root / "automation" / "telemetry" / "2026-07.jsonl").read_text())
            self.assertIn("feed:test", (root / "automation" / "source-health.md").read_text())
            self.assertIn("| feed | 0 | 1 | 0 |", (root / "automation" / "source-lanes.md").read_text())

    def test_slice_daily_month_file_keeps_today_block_only(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "> header\n\n"
            "## 2026-07-02\n\n"
            "### English\n\n"
            "- Signal: today\n"
            "  - Source: https://example.com/today\n\n"
            "## 2026-07-06\n\n"
            "### English\n\n"
            "- Signal: later day\n"
        )
        day = cloud_agent_runner.parse_date("2026-07-02")
        sliced = cloud_agent_runner.slice_daily_month_file(content, day, 50_000)
        self.assertIn("## 2026-07-02", sliced)
        self.assertIn("today", sliced)
        self.assertNotIn("later day", sliced)
        self.assertIn("Context note", sliced)

    def test_slice_daily_month_file_prefers_latest_exact_day_block(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-07-02\n\n"
            "- Signal: old block\n\n"
            "## 2026-07-02 (Screening Pass Integration)\n\n"
            "- Signal: should not pick this\n\n"
            "## 2026-07-02\n\n"
            "- Signal: newest block\n"
        )
        day = cloud_agent_runner.parse_date("2026-07-02")
        sliced = cloud_agent_runner.slice_daily_month_file(content, day, 50_000)
        self.assertIn("newest block", sliced)
        self.assertNotIn("old block", sliced)
        self.assertNotIn("Screening Pass Integration", sliced)

    def test_slice_sources_for_context_keeps_head_and_tail(self) -> None:
        content = "# Sources\n\n## Source Classes\n\n- tiers\n\n" + ("x" * 20_000) + "\n- recent: https://example.com/new\n"
        sliced = cloud_agent_runner.slice_sources_for_context(content, 6_000)
        self.assertIn("Source Classes", sliced)
        self.assertIn("https://example.com/new", sliced)
        self.assertIn("middle sources.md omitted", sliced)
        self.assertLessEqual(len(sliced), 6_100)

    def test_slice_research_log_preserves_candidate_inbox(self) -> None:
        filler = "x" * 30_000
        content = (
            "# Research Log\n\n"
            "intro\n\n"
            f"{filler}\n\n"
            "Candidate inbox, not promoted:\n"
            "- World Model MCP: https://github.com/example/world-model-mcp\n"
            "  - Promotion status: Deferred\n\n"
            f"{filler}\n\n"
            "## 2026-07-06\n\n"
            "Recent pass tail content.\n"
        )
        sliced = cloud_agent_runner.slice_research_log(content, "promote-candidates", 12_000)
        self.assertIn("Candidate inbox", sliced)
        self.assertIn("world-model-mcp", sliced)
        self.assertIn("Recent pass tail content", sliced)

    def test_build_context_daily_skips_weekly_and_slices_daily(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            (root / "docs").mkdir(parents=True)
            (root / "prompts").mkdir(parents=True)
            (root / "prompts" / "runner-rules.md").write_text("# runner rules\n", encoding="utf-8")
            (root / "automation" / "runbook.md").write_text("# runbook\n", encoding="utf-8")
            (root / "docs" / "maintenance.md").write_text("# maintenance\n", encoding="utf-8")
            (root / "prompts" / "daily-update.md").write_text("# prompt\n", encoding="utf-8")
            for name in [
                "sources.md",
                "radar.md",
                "agent-watchlist.md",
                "user-field-notes.md",
                "playbook.md",
                "storage-angle.md",
                "research-log.md",
            ]:
                (root / name).write_text(f"# {name}\n", encoding="utf-8")
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text(
                "# Daily\n\n## 2026-07-02\n\ntoday-content\n\n## 2026-07-06\n\nold-day\n",
                encoding="utf-8",
            )
            (root / "weekly").mkdir(parents=True)
            (root / "weekly" / "2026-W27.md").write_text("weekly-full-content\n", encoding="utf-8")
            day = cloud_agent_runner.parse_date("2026-07-02")
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "openrouter"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "daily", day)
            self.assertIn("today-content", context)
            self.assertNotIn("old-day", context)
            self.assertNotIn("weekly-full-content", context)

    def test_call_openrouter_applies_screening_to_prompt(self) -> None:
        prompt = cloud_agent_runner.build_prompt(
            "daily",
            cloud_agent_runner.parse_date("2026-07-02"),
            ["research-log.md"],
            "repo context",
            public_sources="Public source snapshot:\n- item one",
        )
        screen_payload = {
            "choices": [{"message": {"content": '{"summary":"screened","candidates":[]}'}}]
        }
        main_payload = {
            "choices": [{"message": {"content": '{"summary":"done","updates":[]}'}}]
        }
        with mock.patch.object(
            cloud_agent_runner,
            "call_openrouter_model",
            side_effect=[screen_payload, main_payload],
        ) as model_mock:
            data = cloud_agent_runner.call_openrouter("daily", prompt, "Public source snapshot:\n- item")
        self.assertEqual(cloud_agent_runner.response_output_text(data), '{"summary":"done","updates":[]}')
        main_prompt = model_mock.call_args_list[1].args[0]
        self.assertIn("Screening pass", main_prompt)
        self.assertNotIn("Public source snapshot:", main_prompt)

    def test_shared_screening_reuses_preflight_screen_text(self) -> None:
        payload = {"choices": [{"message": {"content": '{"summary":"ok","updates":[]}'}}]}
        with mock.patch.object(cloud_agent_runner, "task_uses_screening", return_value=True):
            with mock.patch.object(cloud_agent_runner, "invoke_model", return_value=payload) as invoke_mock:
                with mock.patch.object(cloud_agent_runner, "build_context", return_value=(["research-log.md"], "ctx")):
                    with mock.patch.object(cloud_agent_runner, "collect_public_sources", return_value="sources"):
                        with mock.patch.object(cloud_agent_runner, "apply_updates", return_value=0):
                            with tempfile.TemporaryDirectory() as tmp:
                                root = Path(tmp)
                                cloud_agent_runner.run_task(
                                    root,
                                    "source-sweep",
                                    cloud_agent_runner.parse_date("2026-07-02"),
                                    shared_screened=(
                                        '{"summary":"cached-screen","candidates":['
                                        '{"title":"Fresh Signal","evidence":["https://fresh.example/new"],'
                                        '"promotion_status":"candidate"}]}'
                                    ),
                                )
        invoke_mock.assert_called_once()
        expected_screen = (
            '{"summary":"cached-screen","candidates":['
            '{"title":"Fresh Signal","evidence":["https://fresh.example/new"],'
            '"promotion_status":"candidate"}]}'
        )
        self.assertEqual(invoke_mock.call_args.kwargs.get("shared_screened"), expected_screen)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["shared_screening"])

    def test_maintenance_context_excluded_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            (root / "docs").mkdir(parents=True)
            (root / "prompts").mkdir(parents=True)
            (root / "prompts" / "runner-rules.md").write_text("# rules\n", encoding="utf-8")
            (root / "automation" / "runbook.md").write_text("# runbook\n", encoding="utf-8")
            (root / "docs" / "maintenance.md").write_text("maintenance-full-content\n", encoding="utf-8")
            (root / "prompts" / "daily-update.md").write_text("# prompt\n", encoding="utf-8")
            for name in [
                "sources.md",
                "radar.md",
                "agent-watchlist.md",
                "user-field-notes.md",
                "playbook.md",
                "storage-angle.md",
                "research-log.md",
            ]:
                (root / name).write_text(f"# {name}\n", encoding="utf-8")
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text("## 2026-07-02\n\ntoday\n", encoding="utf-8")
            day = cloud_agent_runner.parse_date("2026-07-02")
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "openrouter"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "daily", day)
            self.assertNotIn("maintenance-full-content", context)

    def test_include_maintenance_context_adds_maintenance_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            (root / "docs").mkdir(parents=True)
            (root / "prompts").mkdir(parents=True)
            (root / "prompts" / "runner-rules.md").write_text("# rules\n", encoding="utf-8")
            (root / "automation" / "runbook.md").write_text("# runbook\n", encoding="utf-8")
            (root / "docs" / "maintenance.md").write_text("maintenance-full-content\n", encoding="utf-8")
            (root / "prompts" / "daily-update.md").write_text("# prompt\n", encoding="utf-8")
            for name in ["sources.md", "radar.md", "research-log.md"]:
                (root / name).write_text(f"# {name}\n", encoding="utf-8")
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text("## 2026-07-02\n\ntoday\n", encoding="utf-8")
            day = cloud_agent_runner.parse_date("2026-07-02")
            env = {"AGENT_RADAR_MODEL_PROVIDER": "openrouter", "INCLUDE_MAINTENANCE_CONTEXT": "true"}
            with mock.patch.dict(os.environ, env, clear=False):
                _, context = cloud_agent_runner.build_context(root, "daily", day)
            self.assertIn("maintenance-full-content", context)

    def test_build_screen_prompt_caps_public_sources(self) -> None:
        huge = "Public source snapshot:\n" + ("- item\n" * 20_000)
        prompt = cloud_agent_runner.build_screen_prompt("daily", huge)
        cap = cloud_agent_runner.env_int("MAX_SCREEN_PROMPT_CHARS", cloud_agent_runner.DEFAULT_MAX_SCREEN_PROMPT_CHARS)
        self.assertLessEqual(len(prompt), cap + 10)
        self.assertIn("screening model", prompt)
        self.assertIn("Return only valid JSON", prompt)
        self.assertLess(len(prompt), 2500 + len(huge[:cap]))

    def test_append_telemetry_records_prompt_budget_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cloud_agent_runner.RUN_AUDIT["provider"] = "openrouter"
            cloud_agent_runner.RUN_AUDIT["models"] = ["deepseek/deepseek-v4-pro"]
            cloud_agent_runner.RUN_AUDIT["openrouter_calls"] = 2
            cloud_agent_runner.record_prompt_budget(100_000)
            cloud_agent_runner.RUN_AUDIT["context_chars"] = 90_000
            cloud_agent_runner.RUN_AUDIT["output_chars"] = 5_000
            cloud_agent_runner.RUN_AUDIT["public_source_items"] = 50
            cloud_agent_runner.RUN_AUDIT["collected_source_items"] = 300
            cloud_agent_runner.RUN_AUDIT["started_at"] = time.time()
            day = cloud_agent_runner.parse_date("2026-07-02")
            cloud_agent_runner.append_telemetry(root, "daily", day, 1, "summary", ["source"])
            line = (root / "automation" / "telemetry" / "2026-07.jsonl").read_text(encoding="utf-8")
            self.assertIn('"prompt_budget_ratio": 0.833', line)
            self.assertIn('"prompt_budget_warning": true', line)

    def test_daily_slim_context_excludes_optional_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._seed_minimal_daily_context(root)
            (root / "playbook.md").write_text("playbook-full-content\n", encoding="utf-8")
            (root / "storage-angle.md").write_text("storage-full-content\n", encoding="utf-8")
            (root / "user-field-notes.md").write_text("field-notes-full-content\n", encoding="utf-8")
            day = cloud_agent_runner.parse_date("2026-07-02")
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "openrouter"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "daily", day)
            self.assertNotIn("playbook-full-content", context)
            self.assertNotIn("storage-full-content", context)
            self.assertNotIn("field-notes-full-content", context)

    def test_runbook_excluded_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._seed_minimal_daily_context(root)
            (root / "automation" / "runbook.md").write_text("runbook-full-content\n", encoding="utf-8")
            day = cloud_agent_runner.parse_date("2026-07-02")
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "openrouter"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "daily", day)
            self.assertNotIn("runbook-full-content", context)

    def test_weekly_context_injects_current_week_daily_blocks(self) -> None:
        content = (
            "# Daily Agent Radar - 2026-07\n\n"
            "## 2026-06-30\n\n"
            "- old week\n\n"
            "## 2026-07-02\n\n"
            "- this week one\n\n"
            "## 2026-07-06\n\n"
            "- this week two\n\n"
            "## 2026-07-10\n\n"
            "- next week\n"
        )
        sliced = cloud_agent_runner.slice_daily_month_for_week(
            content,
            cloud_agent_runner.parse_date("2026-07-02"),
            50_000,
        )
        self.assertIn("this week one", sliced)
        self.assertIn("old week", sliced)
        self.assertNotIn("this week two", sliced)
        self.assertNotIn("next week", sliced)
        self.assertIn("ISO week's", sliced)

    def test_weekly_build_context_includes_week_daily_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            day = dt.date(2026, 7, 2)
            self._seed_minimal_weekly_context(root, day)
            (root / "daily" / "2026-07.md").write_text(
                "# Daily\n\n## 2026-07-02\n\nweek-block\n\n## 2026-07-10\n\nlater-week\n",
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "openrouter"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "weekly", day)
            self.assertIn("week-block", context)
            self.assertNotIn("later-week", context)

    def _seed_minimal_daily_context(self, root: Path) -> None:
        (root / "automation").mkdir(parents=True)
        (root / "docs").mkdir(parents=True)
        (root / "prompts").mkdir(parents=True)
        (root / "daily").mkdir(parents=True)
        (root / "prompts" / "runner-rules.md").write_text("# rules\n", encoding="utf-8")
        (root / "automation" / "runbook.md").write_text("# runbook\n", encoding="utf-8")
        (root / "prompts" / "daily-update.md").write_text("# prompt\n", encoding="utf-8")
        for name in ["sources.md", "radar.md", "agent-watchlist.md", "research-log.md"]:
            (root / name).write_text(f"# {name}\n", encoding="utf-8")
        (root / "daily" / "2026-07.md").write_text("## 2026-07-02\n\ntoday-content\n", encoding="utf-8")

    def _seed_minimal_weekly_context(self, root: Path, day: dt.date) -> None:
        (root / "automation").mkdir(parents=True)
        (root / "docs").mkdir(parents=True)
        (root / "prompts").mkdir(parents=True)
        (root / "daily").mkdir(parents=True)
        (root / "weekly").mkdir(parents=True)
        (root / "prompts" / "runner-rules.md").write_text("# rules\n", encoding="utf-8")
        (root / "prompts" / "weekly-review.md").write_text("# prompt\n", encoding="utf-8")
        for name in [
            "sources.md",
            "radar.md",
            "agent-watchlist.md",
            "user-field-notes.md",
            "playbook.md",
            "storage-angle.md",
            "research-log.md",
        ]:
            (root / name).write_text(f"# {name}\n", encoding="utf-8")
        (root / "weekly" / f"{cloud_agent_runner.week_label(day)}.md").write_text("# weekly\n", encoding="utf-8")

    def test_build_prompt_respects_global_prompt_budget(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-02")
        prompt = cloud_agent_runner.build_prompt(
            "weekly",
            day,
            ["research-log.md"],
            "x" * 200_000,
            public_sources="y" * 100_000,
        )
        max_prompt = cloud_agent_runner.env_int(
            "MAX_PROMPT_CHARS", cloud_agent_runner.DEFAULT_MAX_PROMPT_CHARS
        )
        self.assertLessEqual(len(prompt), max_prompt)

    def test_compact_watchlist_for_context_keeps_anchors(self) -> None:
        content = (
            "# Agent Watchlist\n\n"
            "## Mainstream Agents\n\n"
            "## Claude Code\n\n"
            "Status:\n"
            "- Category: Coding agent\n"
            "- Maturity: Active\n"
            "- Recent changes: Security reporting.\n"
            "- Sources: https://example.com\n"
        )
        compact = cloud_agent_runner.compact_watchlist_for_context(content, 10_000)
        self.assertIn("Claude Code", compact)
        self.assertIn("replace_section anchor", compact)
        self.assertNotIn("https://example.com", compact)

    def test_weekly_slim_context_excludes_optional_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            day = dt.date(2026, 7, 2)
            self._seed_minimal_weekly_context(root, day)
            (root / "playbook.md").write_text("playbook-full-content\n", encoding="utf-8")
            (root / "storage-angle.md").write_text("storage-full-content\n", encoding="utf-8")
            (root / "user-field-notes.md").write_text("field-notes-full-content\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "openrouter"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "weekly", day)
            self.assertNotIn("playbook-full-content", context)
            self.assertNotIn("storage-full-content", context)
            self.assertNotIn("field-notes-full-content", context)

    def test_score_source_items_adds_scores_and_sorts(self) -> None:
        items = [
            {"source": "hn", "title": "low signal", "url": "https://example.com/a", "note": ""},
            {"source": "github-release", "title": "agent MCP release", "url": "https://example.com/b", "note": "stars=1200"},
        ]
        scored = cloud_agent_runner.score_source_items(items, None)
        self.assertTrue(cloud_agent_runner.items_are_scored(scored))
        self.assertGreater(int(scored[0]["score"]), int(scored[1]["score"]))

    def test_prepare_shared_source_collection_trims_to_max_task_budget(self) -> None:
        raw = [
            {
                "source": "github",
                "title": f"agent item {index}",
                "url": f"https://example.com/item-{index}",
                "note": "",
            }
            for index in range(150)
        ]
        with mock.patch.object(cloud_agent_runner, "collect_source_items_raw", return_value=(raw, {}, [])):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                with mock.patch.dict(os.environ, {}, clear=True):
                    pool, _lanes, _errors, raw_count = cloud_agent_runner.prepare_shared_source_collection(
                        root,
                        cloud_agent_runner.parse_date("2026-07-02"),
                        ["daily", "source-sweep"],
                    )
                    expected = cloud_agent_runner.public_source_budget("source-sweep")
        self.assertEqual(raw_count, 150)
        self.assertEqual(len(pool), expected)

    def test_warn_public_source_budget_override_prints_when_set(self) -> None:
        with mock.patch.dict(os.environ, {"MAX_PUBLIC_SOURCE_ITEMS": "80"}, clear=False):
            with mock.patch("builtins.print") as print_mock:
                cloud_agent_runner.warn_public_source_budget_override()
        printed = " ".join(str(call.args[0]) for call in print_mock.call_args_list)
        self.assertIn("MAX_PUBLIC_SOURCE_ITEMS", printed)

    def test_shared_daily_collect_keeps_task_budget_after_preflight_pool(self) -> None:
        raw = [
            {
                "source": "github",
                "title": f"agent item {index}",
                "url": f"https://example.com/item-{index}",
                "note": "",
                "score": str(100 - index),
            }
            for index in range(120)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.dict(os.environ, {}, clear=True):
                snapshot = cloud_agent_runner.collect_public_sources_from_cache(
                    raw,
                    {},
                    [],
                    "daily",
                    root,
                    cloud_agent_runner.parse_date("2026-07-02"),
                    raw_collected_count=394,
                )
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["public_source_items"], 50)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["collected_source_items"], 394)
        self.assertIn("Budget 50/120", snapshot)

    def test_compact_screening_for_prompt_is_smaller_than_raw_json(self) -> None:
        raw = json.dumps(
            {
                "summary": "screening summary",
                "candidates": [
                    {
                        "title": f"Candidate {index}",
                        "why_it_matters": "x" * 300,
                        "evidence": [f"https://example.com/{index}"],
                        "promotion_status": "candidate",
                        "relevance_score": 4,
                        "infra_angle": "mcp",
                    }
                    for index in range(20)
                ],
                "gaps": ["gap one", "gap two"],
            }
        )
        compact = cloud_agent_runner.compact_screening_for_prompt(
            raw,
            day=cloud_agent_runner.parse_date("2026-07-02"),
        )
        self.assertLess(len(compact), len(raw) // 2)
        self.assertIn("direction-diversified", compact)
        self.assertIn("Signal-class coverage", compact)
        self.assertIn("no mainstream_product candidates", compact)
        self.assertIn("automation/screening/2026-07-02.json", compact)

    def test_should_skip_source_sweep_when_candidates_already_tracked(self) -> None:
        screen = json.dumps(
            {
                "summary": "done",
                "candidates": [
                    {
                        "title": "Tracked Tool",
                        "evidence": ["https://example.com/tracked"],
                        "promotion_status": "candidate",
                    }
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research-log.md").write_text(
                "https://example.com/tracked\nTracked Tool\n",
                encoding="utf-8",
            )
            skip, reason = cloud_agent_runner.should_skip_source_sweep(root, screen)
        self.assertTrue(skip)
        self.assertIn("already tracked", reason)

    def test_validate_response_size_rejects_huge_payload(self) -> None:
        with mock.patch.dict(os.environ, {"MAX_RESPONSE_CHARS": "100"}, clear=False):
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.validate_response_size("x" * 200)
        self.assertIn("MAX_RESPONSE_CHARS", str(ctx.exception))

    def test_run_task_skips_source_sweep_without_new_candidates(self) -> None:
        screen = json.dumps({"summary": "empty", "candidates": []})
        with mock.patch.object(cloud_agent_runner, "task_uses_screening", return_value=True):
            with mock.patch.object(cloud_agent_runner, "invoke_model") as invoke_mock:
                with mock.patch.object(cloud_agent_runner, "build_context", return_value=(["sources.md"], "ctx")):
                    with mock.patch.object(cloud_agent_runner, "collect_public_sources", return_value="sources"):
                        with tempfile.TemporaryDirectory() as tmp:
                            root = Path(tmp)
                            cloud_agent_runner.run_task(
                                root,
                                "source-sweep",
                                cloud_agent_runner.parse_date("2026-07-02"),
                                shared_screened=screen,
                            )
        invoke_mock.assert_not_called()
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["budget_status"], "skipped-no-new-candidates")

    def test_preflight_writes_screening_artifact(self) -> None:
        payload = {
            "choices": [
                {
                    "message": {
                        "content": '{"summary":"saved","candidates":[{"title":"x","evidence":["https://a"],"promotion_status":"candidate"}]}'
                    }
                }
            ]
        }
        raw_items = [
            {
                "source": "github",
                "title": "agent",
                "url": "https://example.com/a",
                "note": "",
                "score": "10",
            }
        ]
        collection = (raw_items, {}, [], 1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            day = cloud_agent_runner.parse_date("2026-07-02")
            with mock.patch.object(cloud_agent_runner, "call_openrouter_model", return_value=payload):
                screen_text, calls = cloud_agent_runner.preflight_shared_screening(collection, root, day)
            artifact = root / "automation" / "screening" / "2026-07-02.json"
            self.assertEqual(calls, 1)
            self.assertTrue(artifact.exists())
            self.assertIn("saved", artifact.read_text(encoding="utf-8"))
            self.assertIn("saved", screen_text)

    def test_lane_balance_reserves_priority_lanes(self) -> None:
        scored = [
            {"source": "reddit-rss:test", "title": "social", "url": "https://example.com/s", "score": "99"},
            {"source": "github", "title": "repo", "url": "https://example.com/g", "score": "50"},
            {"source": "openai-blog", "title": "official", "url": "https://example.com/o", "score": "40"},
        ]
        selected = cloud_agent_runner.select_scored_items_with_lane_balance(scored, 2)
        lanes = {cloud_agent_runner.source_lane(item["source"]) for item in selected}
        self.assertTrue(lanes & cloud_agent_runner.PRIORITY_BREADTH_LANES)

    def test_enrich_screening_with_ids(self) -> None:
        data = {"candidates": [{"title": "Signal", "evidence": ["https://example.com/x"]}]}
        enriched = cloud_agent_runner.enrich_screening_with_ids(data)
        self.assertTrue(str(enriched["candidates"][0]["id"]).startswith("scr-"))

    def test_rejects_research_log_pass_append(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research-log.md").write_text("# Log\n\n## Candidate inbox\n\n- item\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["research-log.md"],
                    {
                        "updates": [
                            {
                                "path": "research-log.md",
                                "mode": "append",
                                "content": "\n\n### Pass: Daily\n\n- bad\n",
                            }
                        ]
                    },
                )
            self.assertIn("Pass:", str(ctx.exception))

    def test_rejects_radar_update_on_daily_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "radar.md").write_text("# Radar\n\n## Thesis\n\n- old\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.apply_updates(
                    root,
                    ["radar.md"],
                    {"updates": [{"path": "radar.md", "mode": "replace_section", "anchor": "## Thesis", "content": "- new\n"}]},
                    task="daily",
                )
            self.assertIn("radar.md", str(ctx.exception))

    def test_english_block_chinese_block_assembly(self) -> None:
        updates = cloud_agent_runner.normalize_result_updates(
            {
                "updates": [
                    {
                        "path": "daily/2026-07.md",
                        "mode": "append",
                        "day_heading": "## 2026-07-03",
                        "english_block": "#### 1. Signals\n\n- Signal: test\n",
                        "chinese_block": "#### 1. Signals\n\n- 信号：测试\n",
                    }
                ]
            }
        )
        self.assertEqual(len(updates), 1)
        self.assertIn("### English", updates[0]["content"])
        self.assertIn("### 中文", updates[0]["content"])

    def test_compute_synthesis_recall(self) -> None:
        screen = (
            '{"candidates":[{"id":"scr-abc","title":"Fresh MCP","evidence":["https://x"],'
            '"promotion_status":"candidate"}]}'
        )
        result = {
            "summary": "Discussed scr-abc",
            "updates": [{"path": "daily/2026-07.md", "mode": "append", "content": "scr-abc noted"}],
        }
        recall = cloud_agent_runner.compute_synthesis_recall(screen, result)
        self.assertEqual(recall, 1.0)

    def test_diversify_screening_prefers_mainstream_and_user(self) -> None:
        candidates = [
            {"title": f"memory mcp {i}", "infra_angle": "memory", "evidence": [f"https://github.com/x/{i}"]}
            for i in range(8)
        ]
        candidates.insert(
            0,
            {
                "title": "OpenAI Agents changelog",
                "why_it_matters": "Official product preview",
                "evidence": ["https://openai.com/index/agents"],
                "signal_class": "mainstream_product",
            },
        )
        candidates.insert(
            1,
            {
                "title": "Operator field report on review workflow",
                "why_it_matters": "User experience friction",
                "evidence": ["https://example.com/field"],
                "signal_class": "user_workflow",
            },
        )
        ranked = cloud_agent_runner.diversify_screening_candidates(candidates, 6)
        classes = [c.get("signal_class") for c in ranked]
        self.assertIn("mainstream_product", classes)
        self.assertIn("user_workflow", classes)
        self.assertLessEqual(classes.count("infra_primitive"), 3)
        self.assertEqual(classes[0], "mainstream_product")
        self.assertEqual(classes[1], "user_workflow")

    def test_daily_direction_quota_requires_mainstream_or_gap(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Candidate: another memory MCP sandbox\n"
                        "  - Source: https://github.com/example/memory-mcp\n"
                    ),
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("Missing mainstream_product", str(ctx.exception))

    def test_daily_direction_quota_accepts_gaps(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: OpenAI shipped a coding-agent preview.\n"
                        "  - Source: https://openai.com/index/agents\n\n"
                        "#### 7. Gaps\n\n"
                        "- Missing user_workflow: no concrete operator reports in this pass.\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["direction_mainstream"])
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["direction_gaps_present"])

    def test_daily_direction_quota_rejects_attitude_only_user_signal(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: OpenAI shipped a coding-agent preview.\n"
                        "  - Source: https://openai.com/index/agents\n\n"
                        "#### 4. User Field Notes\n\n"
                        "- Signal: users like agents more this week.\n"
                    ),
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("Missing user_workflow", str(ctx.exception))

    def test_daily_direction_quota_accepts_actionable_user_signal(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: OpenAI shipped a coding-agent preview.\n"
                        "  - Source: https://openai.com/index/agents\n\n"
                        "#### 4. User Field Notes\n\n"
                        "- Signal: Claude Code field report: /doctor and Cowork VM-mode.\n"
                        "  - Scenario: operator health checks before long runs.\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["direction_user_workflow"])

    def test_zero_star_infra_repo_is_penalized(self) -> None:
        weak = {
            "source": "github",
            "title": "Tiny memory MCP sandbox",
            "url": "https://github.com/example/tiny-memory-mcp",
            "note": "stars=0",
        }
        strong = {
            "source": "openai-blog",
            "title": "OpenAI Agents changelog preview",
            "url": "https://openai.com/index/agents",
            "note": "",
        }
        weak_score = cloud_agent_runner.score_source_item(weak, {})
        strong_score = cloud_agent_runner.score_source_item(strong, {})
        self.assertGreater(strong_score, weak_score)

    def test_high_confidence_mainstream_prefers_security(self) -> None:
        candidates = [
            {
                "id": "scr-a",
                "title": "OpenAI Codex alpha",
                "confidence": "high",
                "relevance_score": 5,
                "signal_class": "mainstream_product",
                "evidence": ["https://openai.com/codex"],
            },
            {
                "id": "scr-b",
                "title": "China security vulnerabilities in Claude Code",
                "confidence": "high",
                "relevance_score": 5,
                "signal_class": "mainstream_product",
                "infra_angle": "security",
                "evidence": ["https://example.com/claude-security"],
            },
            {
                "id": "scr-c",
                "title": "Random memory MCP",
                "confidence": "high",
                "relevance_score": 5,
                "signal_class": "infra_primitive",
                "evidence": ["https://github.com/x/memory"],
            },
        ]
        must = cloud_agent_runner.high_confidence_mainstream_candidates(candidates)
        self.assertEqual(must[0]["id"], "scr-b")
        self.assertEqual(len(must), 2)

    def test_weighted_and_mainstream_recall(self) -> None:
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "id": "scr-m1",
                        "title": "OpenAI eval framework",
                        "confidence": "high",
                        "signal_class": "mainstream_product",
                        "promotion_status": "candidate",
                        "evidence": ["https://openai.com/eval"],
                    },
                    {
                        "id": "scr-u1",
                        "title": "Operator review workflow note",
                        "confidence": "medium",
                        "signal_class": "user_workflow",
                        "promotion_status": "candidate",
                        "evidence": ["https://example.com/field"],
                    },
                    {
                        "id": "scr-i1",
                        "title": "Tiny sandbox runtime",
                        "confidence": "high",
                        "signal_class": "infra_primitive",
                        "promotion_status": "candidate",
                        "evidence": ["https://github.com/x/sandbox"],
                    },
                ]
            }
        )
        # Cover only mainstream + user; miss infra.
        result = {
            "summary": "Covered OpenAI eval and operator review",
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": "scr-m1 OpenAI eval framework\nscr-u1 Operator review workflow note\n",
                }
            ],
        }
        details = cloud_agent_runner.compute_synthesis_recall_details(screen, result)
        self.assertLess(details["recall"], 1.0)
        self.assertGreaterEqual(details["weighted_recall"], 0.8)
        self.assertEqual(details["mainstream_recall"], 1.0)

    def test_must_cover_rejects_dropped_mainstream(self) -> None:
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "id": "scr-sec",
                        "title": "Security advisories for Claude Code",
                        "confidence": "high",
                        "relevance_score": 5,
                        "signal_class": "mainstream_product",
                        "infra_angle": "security",
                        "promotion_status": "candidate",
                        "evidence": ["https://example.com/claude-advisory"],
                    },
                    {
                        "id": "scr-oa",
                        "title": "OpenAI launches automated evaluations",
                        "confidence": "high",
                        "relevance_score": 5,
                        "signal_class": "mainstream_product",
                        "promotion_status": "candidate",
                        "evidence": ["https://openai.com/evals"],
                    },
                    {
                        "id": "scr-adk",
                        "title": "Google ADK Go 2.0 multi-agent",
                        "confidence": "high",
                        "relevance_score": 5,
                        "signal_class": "mainstream_product",
                        "promotion_status": "candidate",
                        "evidence": ["https://developers.googleblog.com/adk"],
                    },
                ]
            }
        )
        result = {
            "summary": "Only covered OpenAI",
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: OpenAI launches automated evaluations.\n"
                        "  - Source: https://openai.com/evals\n"
                    ),
                }
            ],
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_must_cover_mainstream(result, screen)
        self.assertIn("high-confidence mainstream", str(ctx.exception))

    def test_must_cover_accepts_gaps_explanation(self) -> None:
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "id": "scr-sec",
                        "title": "Security advisories for Claude Code",
                        "confidence": "high",
                        "relevance_score": 5,
                        "signal_class": "mainstream_product",
                        "infra_angle": "security",
                        "promotion_status": "candidate",
                        "evidence": ["https://example.com/claude-advisory"],
                    }
                ]
            }
        )
        result = {
            "summary": "Deferred security item",
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: OpenAI shipped eval tooling.\n"
                        "  - Source: https://openai.com/evals\n\n"
                        "#### 7. Gaps\n\n"
                        "- Dropped: Security advisories for Claude Code (scr-sec) pending corroboration.\n"
                    ),
                }
            ],
        }
        cloud_agent_runner.validate_must_cover_mainstream(result, screen)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["must_cover_missing"], 0)

    def test_stale_roundup_auto_labels_instead_of_rejecting(self) -> None:
        unlabeled = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: GitHub Copilot in VS Code June 2026 releases.\n"
                        "  - Source: https://github.blog/changelog/copilot\n"
                    ),
                }
            ]
        }
        added = cloud_agent_runner.repair_daily_freshness_labels(unlabeled)
        self.assertEqual(added, 1)
        self.assertIn("Freshness: stale-roundup", unlabeled["updates"][0]["content"])
        cloud_agent_runner.validate_daily_freshness(unlabeled)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["stale_roundup_count"], 0)

        already = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: GitHub Copilot in VS Code June 2026 releases.\n"
                        "  - Freshness: stale-roundup\n"
                        "  - Source: https://github.blog/changelog/copilot\n"
                    ),
                }
            ]
        }
        self.assertEqual(cloud_agent_runner.repair_daily_freshness_labels(already), 0)
        cloud_agent_runner.validate_daily_freshness(already)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["stale_roundup_count"], 0)

    def test_compact_screening_lists_must_cover(self) -> None:
        screen = json.dumps(
            {
                "summary": "test",
                "candidates": [
                    {
                        "id": "scr-sec",
                        "title": "Security advisories for Claude Code",
                        "confidence": "high",
                        "relevance_score": 5,
                        "signal_class": "mainstream_product",
                        "infra_angle": "security",
                        "promotion_status": "candidate",
                        "evidence": ["https://example.com/claude-advisory"],
                        "why_it_matters": "Security",
                    },
                    {
                        "id": "scr-oa",
                        "title": "OpenAI launches automated evaluations",
                        "confidence": "high",
                        "relevance_score": 5,
                        "signal_class": "mainstream_product",
                        "promotion_status": "candidate",
                        "evidence": ["https://openai.com/evals"],
                        "why_it_matters": "Eval",
                    },
                ],
            }
        )
        compact = cloud_agent_runner.compact_screening_for_prompt(screen)
        self.assertIn("Must-cover high-confidence mainstream", compact)
        self.assertIn("MUST scr-sec", compact)

    def test_repair_collapsed_relevance_scores(self) -> None:
        candidates = [
            {
                "id": "scr-a",
                "title": "OpenAI eval blog",
                "confidence": "high",
                "relevance_score": 1,
                "signal_class": "mainstream_product",
                "evidence": ["https://openai.com/index/evals"],
                "why_it_matters": "Official eval guidance",
            },
            {
                "id": "scr-b",
                "title": "Tiny sandbox",
                "confidence": "low",
                "relevance_score": 1,
                "signal_class": "infra_primitive",
                "evidence": ["https://github.com/x/sandbox"],
                "why_it_matters": "Early infra",
            },
            {
                "id": "scr-c",
                "title": "Operator field report on review workflow",
                "confidence": "medium",
                "relevance_score": 1,
                "signal_class": "user_workflow",
                "evidence": ["https://example.com/field"],
                "why_it_matters": "Field report: pain point in PR review loop",
            },
        ]
        repaired = cloud_agent_runner.repair_collapsed_relevance_scores(candidates)
        self.assertEqual(repaired, 3)
        scores = [int(c["relevance_score"]) for c in candidates]
        self.assertGreater(max(scores), min(scores))
        self.assertGreater(candidates[0]["relevance_score"], candidates[1]["relevance_score"])

    def test_star_hype_mainstream_demoted_from_must_cover(self) -> None:
        candidates = [
            {
                "id": "scr-stars",
                "title": "Microsoft agent-framework: 11k+ stars",
                "confidence": "high",
                "relevance_score": 9,
                "signal_class": "mainstream_product",
                "evidence": ["https://github.com/microsoft/agent-framework"],
                "why_it_matters": "Official multi-agent framework now at 11k+ stars.",
            },
            {
                "id": "scr-blog",
                "title": "Anthropic containment engineering post",
                "confidence": "high",
                "relevance_score": 8,
                "signal_class": "mainstream_product",
                "infra_angle": "security",
                "evidence": ["https://www.anthropic.com/engineering/how-we-contain-claude"],
                "why_it_matters": "Production containment patterns",
            },
        ]
        self.assertTrue(cloud_agent_runner.is_star_hype_mainstream(candidates[0]))
        self.assertTrue(cloud_agent_runner.demote_star_only_mainstream(candidates[0]))
        self.assertEqual(candidates[0]["confidence"], "medium")
        must = cloud_agent_runner.high_confidence_mainstream_candidates(candidates)
        self.assertEqual([c["id"] for c in must], ["scr-blog"])


if __name__ == "__main__":
    unittest.main()
