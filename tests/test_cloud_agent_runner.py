from __future__ import annotations

import importlib.util
import json
import os
import re
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
    def test_ai_gateway_default_model_route_uses_only_flash_and_pro(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                cloud_agent_runner.ai_gateway_models_for_task("daily"),
                ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
            )
            self.assertEqual(
                cloud_agent_runner.ai_gateway_models_for_task("source-sweep"),
                ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
            )
            self.assertEqual(
                cloud_agent_runner.ai_gateway_models_for_task("weekly"),
                ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
            )
            self.assertEqual(
                cloud_agent_runner.ai_gateway_models_for_task("monthly"),
                ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
            )
            self.assertEqual(
                cloud_agent_runner.ai_gateway_models_for_task("promote-candidates"),
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
            self.assertEqual(cloud_agent_runner.public_source_budget("daily"), 80)
            self.assertEqual(cloud_agent_runner.public_source_budget("source-sweep"), 160)
            self.assertEqual(cloud_agent_runner.public_source_budget("weekly"), 160)
            self.assertEqual(cloud_agent_runner.public_source_budget("monthly"), 200)
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
        # A small limit is floored to the default list size so a stale CI cap
        # cannot silently drop ecosystem repos; nothing beyond that is added.
        with mock.patch.dict(os.environ, {"MAX_RELEASE_REPOS": "3"}, clear=True):
            with mock.patch.object(cloud_agent_runner, "github_repo_exists", return_value=True):
                with tempfile.TemporaryDirectory() as tmp:
                    repos = cloud_agent_runner.release_repos_from_context(Path(tmp), 3)
        self.assertEqual(len(repos), len(cloud_agent_runner.DEFAULT_RELEASE_REPOS))

    def test_ai_gateway_prompt_bans_paid_search_tools(self) -> None:
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

    def test_zero_ai_gateway_budget_dry_runs(self) -> None:
        with mock.patch.dict(os.environ, {"MAX_AI_GATEWAY_CALLS_PER_TASK": "0"}, clear=True):
            data = cloud_agent_runner.call_ai_gateway("daily", "prompt", "sources")
        text = cloud_agent_runner.response_output_text(data)
        self.assertIn("Vercel AI Gateway call budget is zero", text)
        result = json.loads(text)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cloud_agent_runner.apply_updates(Path(tmp), [], result, task="daily"), 0)

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

    def test_reddit_rss_default_batch_covers_all_subreddits(self) -> None:
        # v0.19: default batch (10) covers the full default subreddit list every
        # day — daily rotation blind spots conflicted with social-first sourcing.
        subs = ["a", "b", "c", "d", "e", "f"]
        with mock.patch.object(cloud_agent_runner, "reddit_subreddits", return_value=subs):
            with mock.patch.dict(os.environ, {}, clear=True):
                selected = cloud_agent_runner.reddit_subreddits_for_day(cloud_agent_runner.parse_date("2026-07-02"))
        self.assertEqual(sorted(selected), subs)
        self.assertGreaterEqual(
            cloud_agent_runner.env_int("REDDIT_RSS_BATCH_SIZE", 10),
            len(cloud_agent_runner.DEFAULT_REDDIT_SUBREDDITS),
        )

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
            cloud_agent_runner.RUN_AUDIT["provider"] = "vercel-ai-gateway"
            cloud_agent_runner.RUN_AUDIT["models"] = ["deepseek/deepseek-v4-pro"]
            cloud_agent_runner.RUN_AUDIT["ai_gateway_calls"] = 1
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

            self.assertIn("Vercel AI Gateway calls attempted: 1", (root / "automation" / "runs" / "2026-07.md").read_text())
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
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}, clear=False):
                _, context = cloud_agent_runner.build_context(root, "daily", day)
            self.assertIn("today-content", context)
            self.assertNotIn("old-day", context)
            self.assertNotIn("weekly-full-content", context)

    def test_call_ai_gateway_applies_screening_to_prompt(self) -> None:
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
            "call_ai_gateway_model",
            side_effect=[screen_payload, main_payload],
        ) as model_mock:
            data = cloud_agent_runner.call_ai_gateway("daily", prompt, "Public source snapshot:\n- item")
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
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}, clear=False):
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
            env = {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway", "INCLUDE_MAINTENANCE_CONTEXT": "true"}
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
            cloud_agent_runner.RUN_AUDIT["provider"] = "vercel-ai-gateway"
            cloud_agent_runner.RUN_AUDIT["models"] = ["deepseek/deepseek-v4-pro"]
            cloud_agent_runner.RUN_AUDIT["ai_gateway_calls"] = 2
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
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}, clear=False):
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
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}, clear=False):
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
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}, clear=False):
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
            with mock.patch.dict(os.environ, {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}, clear=False):
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

    def test_prepare_shared_source_collection_uses_screening_pool(self) -> None:
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
        self.assertEqual(raw_count, 150)
        # The screening pool is decoupled from task budgets (SCREEN_POOL_ITEMS,
        # default 240); with 150 raw items the whole collection flows through.
        self.assertEqual(len(pool), 150)

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
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["public_source_items"], 80)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["collected_source_items"], 394)
        self.assertIn("Budget 80/120", snapshot)

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
        # The compact form now carries a Radar Sweep pool for breadth, so it is
        # only required to be smaller than the raw JSON, not half its size.
        self.assertLess(len(compact), len(raw))
        self.assertIn("direction-diversified", compact)
        self.assertIn("Signal-class coverage", compact)
        self.assertIn("Radar Sweep pool (17", compact)
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
            with mock.patch.object(cloud_agent_runner, "call_ai_gateway_model", return_value=payload):
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

    def test_lane_balance_reserves_discussion_lanes(self) -> None:
        # Many high-score GitHub items would otherwise crowd out discussion.
        scored = [
            {
                "source": f"github",
                "title": f"repo-{i}",
                "url": f"https://github.com/example/repo-{i}",
                "score": str(90 - i),
            }
            for i in range(20)
        ] + [
            {
                "source": "bluesky",
                "title": "operator field report",
                "url": "https://bsky.app/profile/example/post/1",
                "score": "30",
            },
            {
                "source": "reddit-rss:LocalLLaMA",
                "title": "claude code pain point thread",
                "url": "https://www.reddit.com/r/LocalLLaMA/comments/abc",
                "score": "28",
            },
            {
                "source": "hacker-news",
                "title": "HN discussion on coding agents",
                "url": "https://news.ycombinator.com/item?id=1",
                "score": "27",
            },
            {
                "source": "openai-blog",
                "title": "official delta",
                "url": "https://openai.com/index/agents",
                "score": "80",
            },
        ]
        selected = cloud_agent_runner.select_scored_items_with_lane_balance(scored, 20)
        discussion = [
            item
            for item in selected
            if cloud_agent_runner.source_lane(item["source"])
            in cloud_agent_runner.DISCUSSION_BREADTH_LANES
        ]
        self.assertGreaterEqual(len(discussion), 2)
        urls = {item["url"] for item in selected}
        self.assertIn("https://bsky.app/profile/example/post/1", urls)
        self.assertIn("https://www.reddit.com/r/LocalLLaMA/comments/abc", urls)
        self.assertGreaterEqual(cloud_agent_runner.RUN_AUDIT.get("discussion_lane_reserved", 0), 2)

    def test_screening_format_lane_balances_discussion(self) -> None:
        items = [
            {
                "source": "github",
                "title": f"repo-{i}",
                "url": f"https://github.com/example/r-{i}",
                "score": str(80 - i),
            }
            for i in range(30)
        ] + [
            {
                "source": "bluesky",
                "title": "field report",
                "url": "https://bsky.app/profile/x/post/2",
                "score": "20",
            }
        ]
        text = cloud_agent_runner.format_scored_items_for_screening(items, 15)
        self.assertIn("bsky.app", text)
        self.assertIn("lane-balanced", text)

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
                        "- Coverage ledger: checked=github-changelog, openai-blog; missed=anthropic, google.\n"
                        "- Missing user_workflow: no concrete operator reports in this pass.\n"
                        "- Missing mainstream_product: Anthropic/Google/Microsoft not covered beyond OpenAI.\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.validate_daily_direction_quota(result)
        # Gap text suppresses the mainstream marker match by design; Gaps still pass the gate.
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["direction_gaps_present"])
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["coverage_ledger_present"])

    def test_daily_gaps_without_coverage_ledger_rejected(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: emerging repo only.\n"
                        "  - Source: https://example.com/repo\n\n"
                        "#### 7. Gaps\n\n"
                        "- Missing user_workflow: no concrete operator reports in this pass.\n"
                        "- Missing mainstream_product: vendors not covered.\n"
                    ),
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("Coverage ledger", str(ctx.exception))

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
                        "- Signal: Anthropic published a containment engineering post.\n"
                        "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
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
                        "- Signal: Anthropic published a containment engineering post.\n"
                        "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
                        "#### 4. User Field Notes\n\n"
                        "- Signal: Claude Code field report: /doctor and Cowork VM-mode.\n"
                        "  - Scenario: operator health checks before long runs.\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["direction_user_workflow"])
        self.assertGreaterEqual(cloud_agent_runner.RUN_AUDIT["vendor_families_covered"], 2)
        self.assertGreaterEqual(cloud_agent_runner.RUN_AUDIT["breadth_themes_covered"], 2)

    def test_infra_cap_warns_when_mainstream_present(self) -> None:
        # Issue #66 (2026-07-18): 5 infra bullets voided an otherwise rich day.
        # With a real mainstream signal the cap must warn, not refuse.
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        infra = "\n\n".join(
            f"- Signal: mcp-memory-tool-{i} adds sandbox memory hooks.\n"
            f"  - Source: https://github.com/example/mcp-memory-{i}"
            for i in range(3)
        )
        content = (
            "## 2026-07-18\n\n### English\n\n"
            "#### 2. New Signals\n\n"
            "- Signal: OpenAI shipped a coding-agent preview.\n"
            "  - Source: https://openai.com/index/agents\n\n"
            "- Signal: Anthropic published a containment engineering post.\n"
            "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
            "#### 4. User Workflow & Field Notes\n\n"
            "- Signal: operator field report: /doctor health checks.\n"
            "  - Scenario: pre-run health checks before long agent sessions.\n\n"
            "#### 5. Emerging Agents / Infra Primitives\n\n"
            f"{infra}\n"
        )
        result = {"updates": [{"path": "daily/2026-07.md", "mode": "append", "content": content}]}
        cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertGreater(cloud_agent_runner.RUN_AUDIT["direction_infra_count"], 2)
        self.assertTrue(
            any("infra_primitive" in w for w in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_infra_cap_still_refuses_without_mainstream(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        infra = "\n\n".join(
            f"- Signal: mcp-memory-tool-{i} adds sandbox memory hooks.\n"
            f"  - Source: https://github.com/example/mcp-memory-{i}"
            for i in range(3)
        )
        content = (
            "## 2026-07-18\n\n### English\n\n"
            "#### 5. Emerging Agents / Infra Primitives\n\n"
            f"{infra}\n\n"
            "#### 8. Assessment & Gaps\n\n"
            "- Coverage ledger: checked=github; missed=vendor pages\n"
            "- Missing mainstream_product: OpenAI/Anthropic pages unreachable\n"
            "- Missing user_workflow: no actionable operator reports\n"
        )
        result = {"updates": [{"path": "daily/2026-07.md", "mode": "append", "content": content}]}
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("infra_primitive", str(ctx.exception))

    def test_radar_sweep_lines_exempt_from_infra_cap(self) -> None:
        # Regression for the v0.18.0 live failure: 7 infra_primitive Radar Sweep
        # one-liners tripped `count_infra_primitive_bullets` and refused the day.
        sweep = "\n".join(
            f"- [infra_primitive] memory-daemon-{i} — MCP sandbox memory tool"
            f" | https://github.com/example/repo{i}"
            for i in range(7)
        )
        content = (
            "## 2026-07-10\n\n### English\n\n"
            "#### 1. Lead Analysis\n\nNarrative paragraph.\n\n"
            "#### 2. New Signals\n\n"
            "- Signal: OpenAI shipped a coding-agent preview.\n"
            "  - Source: https://openai.com/index/agents\n\n"
            "- Signal: Anthropic published a containment engineering post.\n"
            "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
            "#### 4. User Workflow & Field Notes\n\n"
            "- Signal: Claude Code field report: /doctor and Cowork VM-mode.\n"
            "  - Scenario: operator health checks before long runs.\n\n"
            "#### 7. Radar Sweep\n\n"
            f"{sweep}\n\n"
            "#### 8. Assessment & Gaps\n\n"
            "- Coverage ledger: checked=github; missed=none\n"
        )
        result = {
            "updates": [{"path": "daily/2026-07.md", "mode": "append", "content": content}]
        }
        cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["direction_infra_count"], 0)
        # Sanity: without the strip, the same text would blow past the cap.
        self.assertGreater(
            cloud_agent_runner.count_infra_primitive_bullets(content),
            cloud_agent_runner.MAX_DAILY_INFRA_PRIMITIVE_BULLETS,
        )

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

    def test_social_discussion_is_labeled_not_demoted_from_must_cover(self) -> None:
        candidates = [
            {
                "id": "scr-grok",
                "title": "Grok 4.5 launches as cost-efficient coding model",
                "confidence": "high",
                "relevance_score": 8,
                "signal_class": "mainstream_product",
                "evidence": ["https://bsky.app/profile/example/post/1"],
                "why_it_matters": "Disrupts coding agent economics",
            },
            {
                "id": "scr-gh",
                "title": "GitHub Innersource security advisories generally available",
                "confidence": "high",
                "relevance_score": 7,
                "signal_class": "mainstream_product",
                "infra_angle": "security",
                "evidence": [
                    "https://github.blog/changelog/2026-07-08-innersource-security-advisories-are-generally-available"
                ],
                "why_it_matters": "Enterprise advisory distribution",
            },
        ]
        self.assertTrue(cloud_agent_runner.is_social_only_evidence(candidates[0]))
        self.assertTrue(cloud_agent_runner.label_social_discussion_candidate(candidates[0]))
        # Social/discussion stays first-class: confidence kept, evidence labeled.
        self.assertEqual(candidates[0]["confidence"], "high")
        self.assertEqual(candidates[0].get("evidence_basis"), "social_discussion")
        must = cloud_agent_runner.high_confidence_mainstream_candidates(candidates)
        self.assertEqual({c["id"] for c in must}, {"scr-grok", "scr-gh"})
        # Social candidate remains eligible for MUST (not demoted out).
        self.assertIn("scr-grok", {c["id"] for c in must})

    def test_social_discussion_lane_scores_above_generic_github(self) -> None:
        social = {
            "source": "bluesky",
            "title": "Operator field report: Claude Code /doctor pain point",
            "url": "https://bsky.app/profile/example/post/1",
            "note": "discussion thread",
        }
        github = {
            "source": "github",
            "title": "Tiny memory MCP sandbox",
            "url": "https://github.com/example/tiny-memory-mcp",
            "note": "stars=0",
        }
        self.assertGreater(
            cloud_agent_runner.score_source_item(social, {}),
            cloud_agent_runner.score_source_item(github, {}),
        )

    def test_daily_requires_discussion_when_screening_labeled_social(self) -> None:
        cloud_agent_runner.RUN_AUDIT["social_discussion_labeled"] = 2
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        # Actionable user markers that are NOT discussion-host / DISCUSSION_SOURCE_MARKERS.
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
                        "- Signal: Anthropic published a containment engineering post.\n"
                        "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
                        "#### 4. User Field Notes\n\n"
                        "- Signal: Useful trick for agent review loops.\n"
                        "  - Source: https://example.com/internal-note\n"
                    ),
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("social/discussion", str(ctx.exception))

    def test_daily_accepts_bluesky_discussion_coverage(self) -> None:
        cloud_agent_runner.RUN_AUDIT["social_discussion_labeled"] = 1
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
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
                        "- Signal: Anthropic published a containment engineering post.\n"
                        "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
                        "#### 4. User Field Notes\n\n"
                        "- Signal: Useful trick for agent review loops from Bluesky.\n"
                        "  - Source: https://bsky.app/profile/example/post/1\n"
                        "  - Evidence strength: Weak\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["direction_social_discussion"])

    def test_diversify_prefers_discussion_user_workflow(self) -> None:
        candidates = [
            {
                "id": "scr-blog-user",
                "title": "Generic blog user note",
                "confidence": "medium",
                "relevance_score": 8,
                "signal_class": "user_workflow",
                "evidence": ["https://example.com/blog/user-note"],
                "why_it_matters": "Useful trick for review loops in a long blog post",
            },
            {
                "id": "scr-bsky-user",
                "title": "Bluesky operator pain point",
                "confidence": "medium",
                "relevance_score": 5,
                "signal_class": "user_workflow",
                "evidence": ["https://bsky.app/profile/example/post/9"],
                "why_it_matters": "Pain point: /doctor fails mid-session for Claude Code users",
            },
            {
                "id": "scr-m1",
                "title": "OpenAI agents preview",
                "confidence": "high",
                "relevance_score": 9,
                "signal_class": "mainstream_product",
                "evidence": ["https://openai.com/index/agents"],
                "why_it_matters": "Product delta",
            },
            {
                "id": "scr-m2",
                "title": "Anthropic containment",
                "confidence": "high",
                "relevance_score": 8,
                "signal_class": "mainstream_product",
                "evidence": ["https://www.anthropic.com/engineering/how-we-contain-claude"],
                "why_it_matters": "Security post",
            },
        ]
        ranked = cloud_agent_runner.diversify_screening_candidates(candidates, 4)
        ids = [str(c.get("id")) for c in ranked]
        self.assertIn("scr-bsky-user", ids)

    def test_daily_user_gap_mentions_screening_actionable_count(self) -> None:
        cloud_agent_runner.RUN_AUDIT["screening_actionable_user"] = 2
        cloud_agent_runner.RUN_AUDIT["social_discussion_labeled"] = 0
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
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
                        "- Signal: Anthropic published a containment engineering post.\n"
                        "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n\n"
                    ),
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("actionable user_workflow", str(ctx.exception))

    def test_github_repo_user_workflow_reclassified_to_infra(self) -> None:
        cand = {
            "id": "scr-coze",
            "title": "Coze-MCP bridge to OpenClaw",
            "confidence": "low",
            "relevance_score": 4,
            "signal_class": "user_workflow",
            "evidence": ["https://github.com/example/coze-mcp-for-openclaw"],
            "why_it_matters": "User wraps Coze workflows as MCP tools",
        }
        self.assertTrue(cloud_agent_runner.reclassify_repo_as_user_workflow(cand))
        self.assertEqual(cand["signal_class"], "infra_primitive")

    def test_daily_breadth_requires_two_vendor_families(self) -> None:
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
                        "- Signal: Claude Code field report: /doctor.\n"
                        "  - Scenario: operator health checks.\n"
                    ),
                }
            ]
        }
        # Claude marker makes anthropic family too; force openai-only by removing claude wording.
        result["updates"][0]["content"] = (
            "## 2026-07-09\n\n### English\n\n"
            "#### 1. New Signals\n\n"
            "- Signal: OpenAI shipped a coding-agent preview.\n"
            "  - Source: https://openai.com/index/agents\n\n"
            "#### 4. User Field Notes\n\n"
            "- Signal: Operator field report: useful trick for review loops.\n"
            "  - Scenario: PR review with agents.\n"
        )
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_daily_direction_quota(result)
        self.assertIn("2 vendor families", str(ctx.exception))

    def test_warn_dropped_official_urls_on_day_replace(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        old = (
            "## 2026-07-09\n\n"
            "- Signal: Anthropic containment.\n"
            "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n"
        )
        new = (
            "## 2026-07-09\n\n"
            "- Signal: Only OpenAI eval.\n"
            "  - Source: https://openai.com/index/evals\n"
        )
        cloud_agent_runner.warn_dropped_official_urls(old, new, "daily/2026-07.md")
        self.assertTrue(
            any("dropped" in warning and "anthropic.com" in warning for warning in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )


class ContentTruthfulnessTest(unittest.TestCase):
    """v0.8.0 gates: citations, repo reputation, cross-day freshness, templates."""

    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []

    def test_repo_reputation_demotes_suspicious_owner(self) -> None:
        cand = {
            "id": "scr-mem",
            "title": "agent-memory-daemon",
            "confidence": "medium",
            "relevance_score": 6,
            "signal_class": "infra_primitive",
            "evidence": ["https://github.com/Charlesfrederickmenningerdateplum166/agent-memory-daemon"],
            "why_it_matters": "Filesystem-native agent memory daemon",
        }
        self.assertTrue(cloud_agent_runner.demote_low_reputation_repo(cand))
        self.assertEqual(cand["promotion_status"], "defer")
        self.assertEqual(cand["evidence_strength"], "Weak")
        self.assertEqual(cand["confidence"], "low")
        self.assertTrue(any(risk.startswith("suspicious-owner:") for risk in cand["risk_flags"]))

    def test_repo_reputation_keeps_normal_repo(self) -> None:
        cand = {
            "id": "scr-ok",
            "title": "vestige",
            "confidence": "medium",
            "relevance_score": 6,
            "signal_class": "infra_primitive",
            "evidence": ["https://github.com/samvallad33/vestige"],
            "why_it_matters": "Time-travel agent memory",
        }
        self.assertFalse(cloud_agent_runner.demote_low_reputation_repo(cand))
        self.assertNotEqual(cand.get("promotion_status"), "defer")
        # Single-repo evidence still gets a soft risk flag for the promotion gate.
        self.assertIn("single-repo-source", cand.get("risk_flags", []))

    def test_official_blog_evidence_has_no_repo_risks(self) -> None:
        cand = {
            "id": "scr-blog",
            "title": "Anthropic containment",
            "evidence": ["https://www.anthropic.com/engineering/how-we-contain-claude"],
        }
        self.assertEqual(cloud_agent_runner.repo_reputation_risks(cand), [])

    def test_cve_bullet_gets_canonical_nvd_link(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\n"
                        "- Signal: CVE-2026-59723 disclosed in Cline.\n"
                        "  - Source: https://www.thehackerwire.com/vulnerability/CVE-2026-59723/\n"
                    ),
                }
            ]
        }
        labeled = cloud_agent_runner.repair_cve_primary_sources(result)
        self.assertEqual(labeled, 1)
        content = result["updates"][0]["content"]
        self.assertIn("https://nvd.nist.gov/vuln/detail/CVE-2026-59723", content)

    def test_cve_bullet_with_primary_source_untouched(self) -> None:
        content = (
            "## 2026-07-09\n\n### English\n\n"
            "#### 1. New Signals\n\n"
            "- Signal: CVE-2026-59723 disclosed in Cline.\n"
            "  - Source: https://nvd.nist.gov/vuln/detail/CVE-2026-59723\n"
        )
        result = {"updates": [{"path": "daily/2026-07.md", "mode": "append", "content": content}]}
        self.assertEqual(cloud_agent_runner.repair_cve_primary_sources(result), 0)
        self.assertEqual(result["updates"][0]["content"], content)

    def test_verify_emitted_citations_rejects_dead_url(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": "- Signal: x.\n  - Source: https://example.com/gone\n",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(
                cloud_agent_runner, "url_reachability", return_value=("missing", "HTTP 404")
            ):
                with self.assertRaises(SystemExit) as ctx:
                    cloud_agent_runner.verify_emitted_citations(root, result, None)
        self.assertIn("do not resolve", str(ctx.exception))

    def test_verify_emitted_citations_warns_on_unknown(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": "- Signal: x.\n  - Source: https://example.com/maybe\n",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(
                cloud_agent_runner, "url_reachability", return_value=("unknown", "HTTP 403")
            ):
                cloud_agent_runner.verify_emitted_citations(root, result, None)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["citation_urls_unverified"], 1)
        self.assertTrue(
            any("could not be verified" in warning for warning in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_verify_emitted_citations_skips_trusted_snapshot_urls(self) -> None:
        screen = json.dumps(
            {"candidates": [{"title": "x", "evidence": ["https://example.com/known"]}]}
        )
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": "- Signal: x.\n  - Source: https://example.com/known\n",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(cloud_agent_runner, "url_reachability") as reach_mock:
                cloud_agent_runner.verify_emitted_citations(root, result, screen)
        reach_mock.assert_not_called()

    def test_repeated_url_gets_follow_up_label(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-09")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text(
                "## 2026-07-02\n\n- Signal: Sonnet launch.\n"
                "  - Source: https://www.anthropic.com/news/claude-sonnet-5\n\n---\n",
                encoding="utf-8",
            )
            result = {
                "updates": [
                    {
                        "path": "daily/2026-07.md",
                        "mode": "append",
                        "content": (
                            "## 2026-07-09\n\n### English\n\n"
                            "#### 1. New Signals\n\n"
                            "- Signal: Claude Sonnet 5 launches.\n"
                            "  - Source: https://www.anthropic.com/news/claude-sonnet-5\n"
                        ),
                    }
                ]
            }
            labeled = cloud_agent_runner.repair_repeated_url_freshness(result, root, day)
        self.assertEqual(labeled, 1)
        self.assertIn(
            "Freshness: follow-up (previously covered 2026-07-02)",
            result["updates"][0]["content"],
        )

    def test_daily_section_structure_rejects_drifted_sections(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. New Signals\n\ntext\n\n"
                        "#### 2. Public User / Community Signals\n\ntext\n"
                    ),
                }
            ]
        }
        with mock.patch.dict(os.environ, {}, clear=False):
            with self.assertRaises(SystemExit) as ctx:
                cloud_agent_runner.validate_daily_section_structure(result)
        self.assertIn("canonical", str(ctx.exception))

    def test_daily_section_structure_accepts_canonical_template(self) -> None:
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-09\n\n### English\n\n"
                        "#### 1. Lead Analysis\n\ntext\n\n"
                        "#### 2. New Signals\n\ntext\n\n"
                        "#### 6. Storage / Infra Angle\n\ntext\n\n"
                        "#### 7. Radar Sweep\n\n- [x] item | https://example.com\n\n"
                        "#### 8. Assessment & Gaps\n\n"
                        "- Coverage ledger: checked=github; missed=none.\n\n"
                        "### 中文\n\n#### 1. 新信号\n\ntext\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.validate_daily_section_structure(result)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["daily_sections_canonical"])

    def test_weekly_full_requires_scorecard_and_counter_signal(self) -> None:
        result = {
            "updates": [
                {
                    "path": "weekly/2026-W28.md",
                    "mode": "full",
                    "content": "# Weekly\n\n## English\n\n### 1. Product changes\n\ntext\n",
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_weekly_synthesis(result)
        self.assertIn("Thesis Scorecard", str(ctx.exception))
        result["updates"][0]["content"] += "\n### Thesis Scorecard\n\n| 1 | ... | ↑ | e | c |\n"
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_weekly_synthesis(result)
        self.assertIn("Counter-signal", str(ctx.exception))
        result["updates"][0]["content"] += "\n### Signal vs Counter-signal\n\n- pair\n"
        cloud_agent_runner.validate_weekly_synthesis(result)

    def test_weekly_replace_section_not_blocked_by_scorecard_gate(self) -> None:
        result = {
            "updates": [
                {
                    "path": "weekly/2026-W28.md",
                    "mode": "replace_section",
                    "anchor": "### 1. Product changes",
                    "content": "updated bullet\n",
                }
            ]
        }
        cloud_agent_runner.validate_weekly_synthesis(result)

    def test_monthly_full_requires_weekly_coverage(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-15")
        result = {
            "updates": [
                {
                    "path": "monthly/2026-07.md",
                    "mode": "full",
                    "content": "# Monthly\n\n## English\n\ntext\n",
                }
            ]
        }
        with self.assertRaises(SystemExit) as ctx:
            cloud_agent_runner.validate_monthly_synthesis(result, day)
        self.assertIn("Weekly Coverage", str(ctx.exception))
        result["updates"][0]["content"] += "\n### Weekly Coverage\n\n- 2026-W27: ...\n- 2026-W28: ...\n- 2026-W29: ...\n"
        cloud_agent_runner.validate_monthly_synthesis(result, day)
        self.assertTrue(cloud_agent_runner.RUN_AUDIT["monthly_week_coverage_present"])

    def test_iso_weeks_in_month(self) -> None:
        weeks = cloud_agent_runner.iso_weeks_in_month(cloud_agent_runner.parse_date("2026-07-15"))
        self.assertIn("2026-W27", weeks)
        self.assertIn("2026-W29", weeks)

    def test_auto_tasks_monthly_mid_month_refresh(self) -> None:
        tasks = cloud_agent_runner.auto_tasks(cloud_agent_runner.parse_date("2026-07-15"))
        self.assertIn("monthly", tasks)

    def test_thesis_keywords_boost_storage_source_score(self) -> None:
        weights = cloud_agent_runner.thesis_keyword_weights(None)
        plain = {
            "source": "hacker-news",
            "title": "New AI agent framework",
            "url": "https://example.com/a",
            "note": "",
        }
        storage = {
            "source": "hacker-news",
            "title": "New AI agent framework with workspace snapshot and object storage",
            "url": "https://example.com/b",
            "note": "",
        }
        self.assertGreater(
            cloud_agent_runner.score_source_item(storage, {}, weights),
            cloud_agent_runner.score_source_item(plain, {}, weights),
        )

    def test_source_queries_include_china_and_storage_lanes(self) -> None:
        queries = cloud_agent_runner.source_queries_for_task("daily")
        self.assertIn("DeepSeek agent", queries["hn"])
        self.assertIn("agent workspace snapshot", queries["github"])

    def test_source_query_overrides_extend_pool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            (root / "automation" / "source-queries.json").write_text(
                json.dumps({"hn": ["Kimi coding agent"]}), encoding="utf-8"
            )
            queries = cloud_agent_runner.source_queries_for_task("daily", root)
        self.assertIn("Kimi coding agent", queries["hn"])

    def test_candidate_already_tracked_sees_published_dailies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir(parents=True)
            (root / "research-log.md").write_text("# log\n", encoding="utf-8")
            (root / "daily" / "2026-07.md").write_text(
                "## 2026-07-08\n\n- Signal: covered.\n  - Source: https://example.com/covered\n",
                encoding="utf-8",
            )
            cand = {"title": "Something else", "evidence": ["https://example.com/covered"]}
            self.assertTrue(cloud_agent_runner.candidate_already_tracked(root, cand))


class SignalDepthTest(unittest.TestCase):
    """v0.9.0: social upgrades, number checks, storylines, weekly numbers."""

    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []

    def test_multi_platform_social_upgraded_to_strong(self) -> None:
        data = {
            "candidates": [
                {
                    "id": "scr-x",
                    "title": "Claude Cowork mobile expansion",
                    "confidence": "low",
                    "signal_class": "mainstream_product",
                    "evidence": [
                        "https://bsky.app/profile/a/post/1",
                        "https://www.reddit.com/r/ClaudeAI/comments/xyz/",
                    ],
                }
            ]
        }
        enriched = cloud_agent_runner.enrich_social_candidates(data, None)
        cand = enriched["candidates"][0]
        self.assertEqual(cand["corroboration"], "multi-platform")
        self.assertIn("Strong", cand["evidence_strength"])
        self.assertEqual(cand["confidence"], "medium")

    def test_social_mainstream_gets_official_url_attached(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            record = {
                "url": "https://www.anthropic.com/news/claude-cowork-mobile",
                "title": "Claude Cowork mobile expansion for Max subscribers",
                "lane": "official",
            }
            (root / "automation" / "source-cache.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            data = {
                "candidates": [
                    {
                        "id": "scr-y",
                        "title": "Claude Cowork mobile expansion",
                        "confidence": "low",
                        "signal_class": "mainstream_product",
                        "evidence": ["https://bsky.app/profile/a/post/1"],
                    }
                ]
            }
            enriched = cloud_agent_runner.enrich_social_candidates(data, root)
        cand = enriched["candidates"][0]
        self.assertEqual(cand["corroboration"], "official-url-attached")
        self.assertIn("https://www.anthropic.com/news/claude-cowork-mobile", cand["evidence"])

    def test_social_without_official_match_stays_first_class(self) -> None:
        data = {
            "candidates": [
                {
                    "id": "scr-z",
                    "title": "Grok new coding model rumor",
                    "confidence": "medium",
                    "signal_class": "mainstream_product",
                    "evidence": ["https://bsky.app/profile/a/post/2"],
                }
            ]
        }
        enriched = cloud_agent_runner.enrich_social_candidates(data, None)
        cand = enriched["candidates"][0]
        self.assertEqual(cand["corroboration"], "pending-official")
        # No demotion: confidence and class untouched.
        self.assertEqual(cand["confidence"], "medium")
        self.assertEqual(cand["signal_class"], "mainstream_product")

    def test_extract_significant_numbers_filters_noise(self) -> None:
        text = (
            "Grok 4.5 has 1.5T parameters, 500K context, costs $2.5B; "
            "CVE-2026-59723 CVSS 8.8, version 3.0.30, released 2026-07-09, 11.9k stars"
        )
        numbers = cloud_agent_runner.extract_significant_numbers(text)
        self.assertIn(1.5e12, numbers)
        self.assertIn(5e5, numbers)
        self.assertIn(2.5e9, numbers)
        self.assertIn(11.9e3, numbers)
        self.assertNotIn(8.8, numbers)  # CVSS: small, insignificant
        self.assertNotIn(2026.0, numbers)  # year/date stripped

    def test_unverified_number_gets_labeled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            record = {
                "url": "https://bsky.app/profile/a/post/3",
                "title": "Grok 4.5 released",
                "note": "context window 500K",
            }
            (root / "automation" / "source-cache.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            result = {
                "updates": [
                    {
                        "path": "daily/2026-07.md",
                        "mode": "append",
                        "content": (
                            "## 2026-07-09\n\n### English\n\n"
                            "#### 1. New Signals\n\n"
                            "- Signal: Grok 4.5 with 1.5T parameters and 500K context.\n"
                            "  - Source: https://bsky.app/profile/a/post/3\n"
                        ),
                    }
                ]
            }
            labeled = cloud_agent_runner.repair_unverified_numbers(result, root)
        self.assertEqual(labeled, 1)
        content = result["updates"][0]["content"]
        self.assertIn("Number check: 1.5T not found", content)
        # 500K matched the snapshot note, so it is not flagged.
        self.assertNotIn("500", content.split("Number check:")[1])

    def test_supported_numbers_not_labeled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            record = {
                "url": "https://github.com/x/y",
                "title": "sandbox runtime",
                "note": "stars=11900",
            }
            (root / "automation" / "source-cache.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            result = {
                "updates": [
                    {
                        "path": "daily/2026-07.md",
                        "mode": "append",
                        "content": (
                            "## 2026-07-09\n\n"
                            "- Signal: sandbox repo hits 11.9k stars.\n"
                            "  - Source: https://github.com/x/y\n"
                        ),
                    }
                ]
            }
            labeled = cloud_agent_runner.repair_unverified_numbers(result, root)
        self.assertEqual(labeled, 0)

    def test_ongoing_storylines_detects_multi_day_urls(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-09")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text(
                "## 2026-07-03\n\n- Signal: OpenSandbox.\n"
                "  - Source: https://github.com/opensandbox-group/OpenSandbox\n\n---\n\n"
                "## 2026-07-06\n\n- Signal: OpenSandbox again.\n"
                "  - Source: https://github.com/opensandbox-group/OpenSandbox\n\n---\n\n"
                "## 2026-07-08\n\n- Signal: one-off.\n"
                "  - Source: https://example.com/once\n",
                encoding="utf-8",
            )
            storylines = cloud_agent_runner.ongoing_storylines(root, day)
            note = cloud_agent_runner.storylines_prompt_note(root, day)
        self.assertEqual(len(storylines), 1)
        url, count, last = storylines[0]
        self.assertIn("opensandbox", url)
        self.assertEqual(count, 2)
        self.assertEqual(last, "2026-07-06")
        self.assertIn("Freshness: follow-up", note)

    def test_weekly_numbers_note_aggregates_telemetry(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-09")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation" / "telemetry").mkdir(parents=True)
            records = [
                {
                    "date": "2026-07-08",
                    "task": "daily",
                    "vendor_families_covered": 6,
                    "breadth_themes_covered": 4,
                    "mainstream_recall": 0.8,
                    "repeat_url_labeled": 1,
                    "citation_urls_unreachable": 0,
                    "numeric_claims_flagged": 2,
                    "repo_reputation_demoted": 0,
                    "social_discussion_labeled": 3,
                },
                {"date": "2026-07-08", "task": "source-sweep"},
                {
                    "date": "2026-07-02",
                    "task": "daily",
                    "vendor_families_covered": 4,
                    "breadth_themes_covered": 3,
                    "mainstream_recall": 0.5,
                    "repeat_url_labeled": 0,
                    "citation_urls_unreachable": 0,
                    "numeric_claims_flagged": 0,
                    "repo_reputation_demoted": 0,
                    "social_discussion_labeled": 1,
                },
            ]
            (root / "automation" / "telemetry" / "2026-07.jsonl").write_text(
                "\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8"
            )
            note = cloud_agent_runner.weekly_numbers_note(root, day)
        self.assertIn("By the Numbers", note)
        self.assertIn("avg_vendor_families: 6", note)
        self.assertIn("prev week: 4", note)

    def test_candidate_id_is_url_canonical(self) -> None:
        base = {
            "confidence": "medium",
            "signal_class": "infra_primitive",
            "evidence": ["https://github.com/x/y"],
        }
        first = cloud_agent_runner.enrich_screening_with_ids(
            {"candidates": [dict(base, title="Title one")]}
        )["candidates"][0]["id"]
        second = cloud_agent_runner.enrich_screening_with_ids(
            {"candidates": [dict(base, title="A different title")]}
        )["candidates"][0]["id"]
        self.assertEqual(first, second)

    def test_research_log_duplicate_url_warns(self) -> None:
        old = "## Candidate inbox\n\n- **Old entry** (scr-a): https://example.com/tracked\n"
        content = "\n- **New duplicate** (scr-b): https://example.com/tracked\n"
        cloud_agent_runner.validate_research_log_append(old, content)
        self.assertTrue(
            any("already-tracked" in warning for warning in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_breadth_feeds_include_hf_but_no_simplified_chinese_media(self) -> None:
        names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_FEEDS]
        self.assertIn("hf-blog", names)
        self.assertNotIn("jiqizhixin", names)

    def test_simplified_chinese_media_url_penalized(self) -> None:
        base = {"source": "hacker-news", "title": "AI agent launch coverage", "note": ""}
        chinese_media = dict(base, url="https://www.jiqizhixin.com/articles/agent-launch")
        neutral = dict(base, url="https://example.com/agent-launch")
        self.assertLess(
            cloud_agent_runner.score_source_item(chinese_media, {}),
            cloud_agent_runner.score_source_item(neutral, {}),
        )

    def test_official_china_vendor_pages_not_penalized(self) -> None:
        base = {"source": "qwen-blog", "title": "Qwen coding agent update", "note": ""}
        vendor = dict(base, url="https://qwenlm.github.io/blog/qwen-agent")
        score = cloud_agent_runner.score_source_item(vendor, {})
        self.assertGreater(score, 20)  # official lane weight intact, no media penalty


class TransportResilienceTest(unittest.TestCase):
    def test_ai_gateway_request_uses_vercel_endpoint_and_api_key(self) -> None:
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "{\"summary\": \"ok\"}"}}]}
        ).encode("utf-8")
        with mock.patch.dict(
            os.environ,
            {"AI_GATEWAY_API_KEY": "vercel-key", "AI_GATEWAY_FALLBACK_MODELS": ""},
            clear=False,
        ):
            with mock.patch.object(urllib.request, "urlopen", return_value=response) as urlopen_mock:
                cloud_agent_runner.call_ai_gateway_model("prompt", "deepseek/deepseek-v4-flash")
        request = urlopen_mock.call_args.args[0]
        self.assertEqual(request.full_url, "https://ai-gateway.vercel.sh/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer vercel-key")
        self.assertIsNone(request.get_header("Http-referer"))
        payload = json.loads(request.data.decode("utf-8"))
        self.assertNotIn("response_format", payload)

    def test_ai_gateway_call_retries_incomplete_read(self) -> None:
        # Issue #59: a response body cut mid-read (http.client.IncompleteRead)
        # crashed the daily task instead of falling through the retry chain.
        import http.client as http_client
        import io

        good = mock.MagicMock()
        good.__enter__.return_value.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "{\"summary\": \"ok\"}"}}]}
        ).encode("utf-8")
        with mock.patch.dict(
            os.environ,
            {"AI_GATEWAY_API_KEY": "x", "AI_GATEWAY_FALLBACK_MODELS": "model-b"},
            clear=False,
        ):
            with mock.patch.object(
                urllib.request,
                "urlopen",
                side_effect=[http_client.IncompleteRead(b"y" * 10), good],
            ):
                with mock.patch.object(cloud_agent_runner.time, "sleep"):
                    parsed = cloud_agent_runner.call_ai_gateway_model("prompt", "model-a")
        self.assertIn("choices", parsed)

    def test_max_response_chars_generous_for_all_tasks(self) -> None:
        # Issue #59 round 3: the daily legitimately produced 75.3k chars under
        # the v0.19 funnel; every task now gets the 96k cap by default.
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(cloud_agent_runner.max_response_chars("daily"), 96_000)
            self.assertEqual(cloud_agent_runner.max_response_chars("weekly"), 96_000)
            self.assertEqual(cloud_agent_runner.max_response_chars("monthly"), 96_000)
        cloud_agent_runner.validate_response_size("x" * 80_000, "daily")
        with self.assertRaises(SystemExit):
            cloud_agent_runner.validate_response_size("x" * 100_000, "daily")


class AuditLoopTest(unittest.TestCase):
    """v0.10.0: sharded screening, claim audit, direction-asset injection."""

    def setUp(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []

    def test_screening_shard_split_by_lane(self) -> None:
        items = [
            {"source": "github", "title": "repo", "url": "https://github.com/a/b"},
            {"source": "bluesky", "title": "post", "url": "https://bsky.app/p/1"},
            {"source": "hacker-news", "title": "thread", "url": "https://news.ycombinator.com/item?id=1"},
            {"source": "openai-blog", "title": "release", "url": "https://openai.com/x"},
            {"source": "npm", "title": "package", "url": "https://www.npmjs.com/package/x"},
        ]
        shards = dict(cloud_agent_runner.screening_shard_items(items))
        self.assertEqual(len(shards["discussion"]), 2)
        self.assertEqual(len(shards["official-vendor"]), 1)
        self.assertEqual(len(shards["github-oss"]), 1)
        self.assertEqual(len(shards["packages"]), 1)

    def test_merge_screening_payloads_dedupes_by_url(self) -> None:
        merged = cloud_agent_runner.merge_screening_payloads(
            [
                {
                    "summary": "official",
                    "candidates": [
                        {"title": "A", "evidence": ["https://example.com/a"]},
                        {"title": "B", "evidence": ["https://example.com/b"]},
                    ],
                    "gaps": ["Missing user_workflow: x"],
                },
                {
                    "summary": "discussion",
                    "candidates": [
                        {"title": "A retitled", "evidence": ["https://example.com/a"]},
                        {"title": "C", "evidence": ["https://bsky.app/p/1"]},
                    ],
                    "gaps": ["Missing user_workflow: x", "Missing mainstream_product: y"],
                },
            ]
        )
        titles = [cand["title"] for cand in merged["candidates"]]
        self.assertEqual(titles, ["A", "B", "C"])
        self.assertEqual(len(merged["gaps"]), 2)
        self.assertIn("official", merged["summary"])
        self.assertIn("discussion", merged["summary"])

    def test_preflight_shards_screening_calls(self) -> None:
        items = [
            {"source": "github", "title": "repo", "url": "https://github.com/a/b", "score": "10"},
            {"source": "bluesky", "title": "post", "url": "https://bsky.app/p/1", "score": "10"},
        ]
        payloads = [
            {"choices": [{"message": {"content": json.dumps({"summary": "s1", "candidates": [{"title": "A", "evidence": ["https://github.com/a/b"]}], "gaps": []})}}]},
            {"choices": [{"message": {"content": json.dumps({"summary": "s2", "candidates": [{"title": "B", "evidence": ["https://bsky.app/p/1"]}], "gaps": []})}}]},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation" / "screening").mkdir(parents=True)
            (root / "prompts").mkdir(parents=True)
            (root / "prompts" / "screening-schema.md").write_text("# schema\n", encoding="utf-8")
            with mock.patch.object(
                cloud_agent_runner, "call_ai_gateway_model", side_effect=payloads
            ) as model_mock:
                screen_text, calls = cloud_agent_runner.preflight_shared_screening(
                    ([dict(item) for item in items], {}, [], 2),
                    root,
                    cloud_agent_runner.parse_date("2026-07-10"),
                )
        self.assertEqual(calls, 2)
        self.assertEqual(model_mock.call_count, 2)
        data = json.loads(screen_text)
        self.assertEqual(len(data["candidates"]), 2)

    def test_claim_audit_labels_flagged_bullet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            record = {
                "url": "https://bsky.app/p/9",
                "title": "Copilot desktop app preview discussion",
                "note": "preview build feedback",
            }
            (root / "automation" / "source-cache.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            result = {
                "updates": [
                    {
                        "path": "daily/2026-07.md",
                        "mode": "append",
                        "content": (
                            "## 2026-07-10\n\n### English\n\n"
                            "#### 1. New Signals\n\n"
                            "- Signal: Copilot desktop app is generally available.\n"
                            "  - Source: https://bsky.app/p/9\n"
                        ),
                    }
                ]
            }
            audit_payload = {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {"flags": [{"bullet": 1, "reason": "source says preview, bullet says GA"}]}
                            )
                        }
                    }
                ]
            }
            env = {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}
            with mock.patch.dict(os.environ, env, clear=False):
                with mock.patch.object(
                    cloud_agent_runner, "call_ai_gateway_model", return_value=audit_payload
                ):
                    labeled = cloud_agent_runner.run_claim_audit(root, "daily", result)
        self.assertEqual(labeled, 1)
        self.assertIn("Claim audit: source says preview", result["updates"][0]["content"])

    def test_claim_audit_fails_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "automation").mkdir(parents=True)
            record = {"url": "https://bsky.app/p/9", "title": "t", "note": "n"}
            (root / "automation" / "source-cache.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            result = {
                "updates": [
                    {
                        "path": "daily/2026-07.md",
                        "mode": "append",
                        "content": "- Signal: x.\n  - Source: https://bsky.app/p/9\n",
                    }
                ]
            }
            env = {"AGENT_RADAR_MODEL_PROVIDER": "vercel-ai-gateway"}
            with mock.patch.dict(os.environ, env, clear=False):
                with mock.patch.object(
                    cloud_agent_runner,
                    "call_ai_gateway_model",
                    side_effect=RuntimeError("model down"),
                ):
                    labeled = cloud_agent_runner.run_claim_audit(root, "daily", result)
        self.assertEqual(labeled, 0)
        self.assertTrue(
            any("Claim audit skipped" in warning for warning in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_radar_open_questions_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "radar.md").write_text(
                "# Radar\n\n## Current Thesis\n\n1. X.\n\n## Open Questions\n\n"
                "- Will MCP become the default?\n- Who pays for agent storage?\n",
                encoding="utf-8",
            )
            questions = cloud_agent_runner.radar_open_questions(root)
        self.assertEqual(len(questions), 2)
        self.assertIn("Will MCP become the default?", questions)

    def test_stale_watchlist_entries_detected(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-10")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "agent-watchlist.md").write_text(
                "# Agent Watchlist\n\n"
                "## Fresh Agent\n\n- Updated: 2026-07-08 with news\n\n"
                "## Old Agent\n\n- Updated: 2026-06-01 long ago\n\n"
                "## Undated Agent\n\n- No dates here\n",
                encoding="utf-8",
            )
            stale = cloud_agent_runner.stale_watchlist_entries(root, day)
        self.assertEqual(len(stale), 2)
        self.assertTrue(any("Old Agent" in entry for entry in stale))
        self.assertTrue(any("Undated Agent (undated)" in entry for entry in stale))

    def test_corroboration_queue_collects_labels(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-10")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text(
                "## 2026-07-09\n\n"
                "- Signal: Grok 4.5 claims.\n"
                "  - Number check: 1.5T not found in cited snapshot source; verify before trusting.\n\n"
                "- Signal: clean bullet.\n"
                "  - Source: https://example.com/ok\n",
                encoding="utf-8",
            )
            queue = cloud_agent_runner.corroboration_queue(root, day)
        self.assertEqual(len(queue), 1)
        self.assertIn("Grok 4.5", queue[0])

    def test_shared_screening_preserves_shard_count_in_run_task(self) -> None:
        payload = {"choices": [{"message": {"content": '{"summary":"ok","updates":[]}'}}]}
        cloud_agent_runner.RUN_AUDIT["screening_shards"] = 2
        with mock.patch.object(cloud_agent_runner, "task_uses_screening", return_value=True):
            with mock.patch.object(cloud_agent_runner, "invoke_model", return_value=payload):
                with mock.patch.object(cloud_agent_runner, "build_context", return_value=(["research-log.md"], "ctx")):
                    with mock.patch.object(cloud_agent_runner, "collect_public_sources", return_value="sources"):
                        with mock.patch.object(cloud_agent_runner, "apply_updates", return_value=0):
                            with tempfile.TemporaryDirectory() as tmp:
                                cloud_agent_runner.run_task(
                                    Path(tmp),
                                    "source-sweep",
                                    cloud_agent_runner.parse_date("2026-07-02"),
                                    shared_screened=(
                                        '{"summary":"s","candidates":['
                                        '{"title":"Fresh","evidence":["https://fresh.example/x"],'
                                        '"promotion_status":"candidate"}]}'
                                    ),
                                    preflight_screen_calls=2,
                                )
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["screening_shards"], 2)

    def test_mainstream_recall_denominator_capped_after_sharding(self) -> None:
        candidates = []
        for index in range(9):
            candidates.append(
                {
                    "id": f"scr-m{index}",
                    "title": f"OpenAI mainstream delta number{index}",
                    "confidence": "high",
                    "relevance_score": 10 - index,
                    "signal_class": "mainstream_product",
                    "evidence": [f"https://openai.com/news/delta-{index}"],
                }
            )
        screen = json.dumps({"candidates": candidates})
        # Cover the top 4 by priority: recall over a capped pool of 6 => 0.667,
        # not 4/9 = 0.444 over the whole merged shard pool.
        covered = "\n".join(
            f"- Signal: OpenAI mainstream delta number{index}.\n"
            f"  - Source: https://openai.com/news/delta-{index}"
            for index in range(4)
        )
        result = {
            "summary": "daily",
            "updates": [
                {"path": "daily/2026-07.md", "mode": "append", "content": covered}
            ],
        }
        details = cloud_agent_runner.compute_synthesis_recall_details(screen, result)
        self.assertGreaterEqual(details["mainstream_recall"], 0.5)

    def test_secret_scan_pattern_has_sk_boundary(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "cloud-agent.yml").read_text(encoding="utf-8")
        match = re.search(r"grep -RInE [^']*'(\(.*ANTHROPIC_API_KEY\\s\*=\))'", workflow)
        assert match is not None
        pattern = re.compile(match.group(1))
        self.assertIsNone(
            pattern.search(
                "https://github.blog/changelog/2026-07-09-ask-copilot-for-a-repository-overview"
            )
        )
        self.assertIsNone(pattern.search("- **Ask HN thread** (scr-ask-hn-hate-coding-agents): note"))
        # Assemble the fake key at runtime so this test file itself never
        # contains a full `sk-...` string for the workflow scan to flag.
        fake_key = "sk-" + "AbCdEfGhIjKlMnOpQrStUvWx"
        self.assertIsNotNone(pattern.search(f"api_key = {fake_key}"))

    def test_must_cover_skips_already_published_story(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-10")
        screen = json.dumps(
            {
                "candidates": [
                    {
                        "id": "scr-contain",
                        "title": "How Anthropic contains Claude across products",
                        "confidence": "high",
                        "relevance_score": 9,
                        "signal_class": "mainstream_product",
                        "evidence": ["https://www.anthropic.com/engineering/how-we-contain-claude"],
                    }
                ]
            }
        )
        result = {
            "summary": "daily",
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": "- Signal: something fresh today.\n  - Source: https://example.com/new\n",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir(parents=True)
            (root / "daily" / "2026-07.md").write_text(
                "## 2026-07-09\n\n- Signal: Anthropic containment post.\n"
                "  - Source: https://www.anthropic.com/engineering/how-we-contain-claude\n",
                encoding="utf-8",
            )
            # Story already published on 07-09: no longer a MUST for 07-10.
            cloud_agent_runner.validate_must_cover_mainstream(result, screen, root=root, day=day)
        # Without publication history the same candidate is still required.
        with self.assertRaises(SystemExit):
            cloud_agent_runner.validate_must_cover_mainstream(result, screen)

    def test_model_call_timeout_tiered_by_model(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                cloud_agent_runner.model_call_timeout("deepseek/deepseek-v4-flash"), 300
            )
            self.assertEqual(cloud_agent_runner.model_call_timeout("deepseek/deepseek-v4-pro"), 900)

    def test_audit_daily_depth_flags_thin_day(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-10\n\n### English\n\n"
                        "#### 1. Lead Analysis\n\n"
                        "One short line.\n\n"
                        "#### 2. New Signals\n\n"
                        "- Signal: only one thin signal.\n"
                        "  - Source: https://example.com/a\n\n"
                        "#### 6. Storage / Infra Angle\n\n"
                        "- Signal: single storage bullet without trigger.\n\n"
                        "#### 8. Assessment & Gaps\n\n"
                        "- Coverage ledger: checked=github; missed=none\n\n"
                        "### 中文\n\n#### 1. 新信号\n\n- 信号：略。\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.audit_daily_depth(result)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["daily_signal_count"], 1)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["storage_angle_bullets"], 1)
        warnings = cloud_agent_runner.RUN_AUDIT["apply_warnings"]
        self.assertTrue(any("New Signals (target 6-8)" in w for w in warnings))
        self.assertTrue(any("Storage / Infra Angle has 1" in w for w in warnings))
        self.assertTrue(any("Lead Analysis is thin" in w for w in warnings))
        self.assertTrue(any("Radar Sweep has only 0" in w for w in warnings))

    def test_audit_daily_depth_quiet_on_deep_day(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        signals = "\n\n".join(
            f"- Signal: item {index}.\n"
            f"  - Why it matters: mechanism {index}.\n"
            f"  - Evidence strength: Strong.\n"
            f"  - So what: watch vendor {index} pricing.\n"
            f"  - Source: https://example.com/{index}"
            for index in range(6)
        )
        lead = (
            "Today's dominant storyline is the convergence of sandbox checkpointing and "
            "agent memory: three vendors shipped snapshot-adjacent features within 24 "
            "hours, which strengthens thesis 4 while the pricing counter-signal from "
            "operators on HN cuts against thesis 10.\n\n"
            "The second thread is eval infrastructure consolidating around trace replay; "
            "if a second enterprise vendor names replay in a changelog this week, the "
            "storage angle moves from speculative to confirmed. Evidence conflicts on "
            "adoption speed: vendor blogs claim production use, operator threads report "
            "pilot-stage friction and cost overruns."
        )
        sweep = "\n".join(
            f"- [infra_primitive] Sweep item {index} — one-line why | https://example.com/s{index}"
            for index in range(8)
        )
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-10\n\n### English\n\n"
                        "#### 1. Lead Analysis\n\n"
                        f"{lead}\n\n"
                        "#### 2. New Signals\n\n"
                        f"{signals}\n\n"
                        "#### 6. Storage / Infra Angle\n\n"
                        "- Signal: snapshots standardizing.\n"
                        "  - Watch trigger: a second vendor ships checkpoint APIs.\n"
                        "- Signal: replay demand rising.\n"
                        "  - Watch trigger: replay named in an enterprise changelog.\n\n"
                        "#### 7. Radar Sweep\n\n"
                        f"{sweep}\n\n"
                        "#### 8. Assessment & Gaps\n\n"
                        "- Coverage ledger: checked=github; missed=none\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.audit_daily_depth(result)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["daily_signal_count"], 6)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["storage_angle_bullets"], 2)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["radar_sweep_count"], 8)
        self.assertGreaterEqual(cloud_agent_runner.RUN_AUDIT["lead_analysis_chars"], 400)
        self.assertFalse(
            any(
                "Daily depth" in w or "Daily breadth" in w
                for w in cloud_agent_runner.RUN_AUDIT["apply_warnings"]
            )
        )

    def test_ecosystem_vendors_count_as_mainstream(self) -> None:
        for text in ("Grok 4.5 coding update", "Vercel AI SDK 6 released", "E2B sandbox templates", "OpenCode v1.2"):
            self.assertTrue(
                any(m in text.lower() for m in cloud_agent_runner.MAINSTREAM_VENDOR_MARKERS),
                text,
            )
        families = cloud_agent_runner.vendor_families_in_text(
            "Vercel shipped agents; Cloudflare Workers AI update; ampcode chronicle; OpenCode release; E2B fork"
        )
        for family in ("vercel", "cloudflare", "amp", "opencode", "e2b"):
            self.assertIn(family, families)

    def test_vendor_zero_coverage_names_dark_vendors(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        items = [
            {"source": "openai-blog", "title": "OpenAI codex update", "url": "https://openai.com/x", "note": ""},
            {"source": "github", "title": "Cursor 2.0 changelog", "url": "https://cursor.com/changelog", "note": ""},
        ]
        gaps = cloud_agent_runner.record_vendor_zero_coverage(items)
        self.assertIn("xai", gaps)
        self.assertIn("vercel", gaps)
        self.assertNotIn("openai", gaps)
        self.assertNotIn("cursor", gaps)
        self.assertTrue(
            any("Zero collected items" in w for w in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_release_repos_env_extends_defaults(self) -> None:
        with mock.patch.dict(os.environ, {"RELEASE_REPOS": "someorg/custom-agent"}, clear=False):
            with mock.patch.object(cloud_agent_runner, "github_repo_exists", return_value=True):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    repos = cloud_agent_runner.release_repos_from_context(root, 30)
        self.assertIn("sst/opencode", repos)
        self.assertIn("e2b-dev/E2B", repos)
        self.assertIn("someorg/custom-agent", repos)

    def test_ecosystem_release_repos_in_defaults(self) -> None:
        for repo in ("sst/opencode", "e2b-dev/E2B", "vercel/ai", "cloudflare/agents", "anthropics/claude-code"):
            self.assertIn(repo, cloud_agent_runner.DEFAULT_RELEASE_REPOS)
        names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_PAGES]
        self.assertIn("xai-news", names)
        self.assertIn("e2b-blog", names)

    def test_breadth_sources_expanded(self) -> None:
        feed_names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_FEEDS]
        for name in ("simonwillison", "latent-space", "supabase-blog", "flyio-blog", "producthunt"):
            self.assertIn(name, feed_names)
        page_names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_PAGES]
        for name in ("mistral-news", "github-trending"):
            self.assertIn(name, page_names)
        self.assertGreaterEqual(len(cloud_agent_runner.DEFAULT_REDDIT_SUBREDDITS), 10)

    def test_expert_lane_scores_high(self) -> None:
        self.assertEqual(cloud_agent_runner.source_lane("simonwillison"), "expert")
        expert = {"source": "simonwillison", "title": "Notes on coding agent evals", "url": "https://simonwillison.net/x", "note": ""}
        generic = {"source": "some-feed", "title": "Notes on coding agent evals", "url": "https://example.com/x", "note": ""}
        self.assertGreater(
            cloud_agent_runner.score_source_item(expert, {}),
            cloud_agent_runner.score_source_item(generic, {}),
        )

    def test_second_ecosystem_sweep_in_defaults(self) -> None:
        for repo in (
            "All-Hands-AI/OpenHands",
            "browser-use/browser-use",
            "block/goose",
            "continuedev/continue",
            "RooCodeInc/Roo-Code",
            "zed-industries/zed",
            "letta-ai/letta",
            "mem0ai/mem0",
            "langfuse/langfuse",
            "pydantic/pydantic-ai",
        ):
            self.assertIn(repo, cloud_agent_runner.DEFAULT_RELEASE_REPOS)
        page_names = [name for name, _ in cloud_agent_runner.DEFAULT_CHANGELOG_PAGES]
        for name in ("modal-blog", "daytona-blog", "openrouter-announcements", "meta-ai-blog"):
            self.assertIn(name, page_names)
        for pkg in ("pydantic-ai", "mem0ai", "langfuse", "browser-use", "smolagents"):
            self.assertIn(pkg, cloud_agent_runner.DEFAULT_PYPI_PACKAGES)

    def test_anchored_markers_avoid_substring_false_positives(self) -> None:
        # "zed"/"modal"/"manus" as bare substrings would match ordinary words.
        for text in ("we analyzed the results", "a multimodal benchmark", "the manuscript was updated"):
            self.assertFalse(
                any(m in text for m in cloud_agent_runner.MAINSTREAM_VENDOR_MARKERS), text
            )
        for text in ("zed-industries ships agentic editing", "modal.com sandbox update", "manus ai general agent"):
            self.assertTrue(
                any(m in text for m in cloud_agent_runner.MAINSTREAM_VENDOR_MARKERS), text
            )

    def test_release_repo_limit_always_fits_defaults(self) -> None:
        with mock.patch.dict(os.environ, {"MAX_RELEASE_REPOS": "5", "GITHUB_API_MIN_INTERVAL": "0"}, clear=False):
            with mock.patch.object(cloud_agent_runner, "github_repo_exists", return_value=True):
                with tempfile.TemporaryDirectory() as tmp:
                    repos = cloud_agent_runner.release_repos_from_context(Path(tmp), 5)
        self.assertGreaterEqual(len(repos), len(cloud_agent_runner.DEFAULT_RELEASE_REPOS))

    def test_discussion_shard_runs_first(self) -> None:
        items = [
            {"source": "github", "title": "repo", "url": "https://github.com/a/b"},
            {"source": "bluesky", "title": "post", "url": "https://bsky.app/p/1"},
        ]
        shards = cloud_agent_runner.screening_shard_items(items)
        self.assertEqual(shards[0][0], "discussion")

    def test_diversify_reserves_three_discussion_user_slots(self) -> None:
        candidates = []
        for index in range(4):
            candidates.append(
                {
                    "id": f"scr-m{index}",
                    "title": f"OpenAI delta {index}",
                    "confidence": "high",
                    "relevance_score": 10,
                    "signal_class": "mainstream_product",
                    "evidence": [f"https://openai.com/news/{index}"],
                }
            )
        for index in range(4):
            candidates.append(
                {
                    "id": f"scr-d{index}",
                    "title": f"Operator field report {index}",
                    "confidence": "medium",
                    "relevance_score": 6,
                    "signal_class": "user_workflow",
                    "evidence": [f"https://www.reddit.com/r/ClaudeAI/comments/{index}/"],
                    "why_it_matters": f"Pain point {index} with concrete detail",
                }
            )
        for index in range(6):
            candidates.append(
                {
                    "id": f"scr-i{index}",
                    "title": f"infra repo {index}",
                    "confidence": "medium",
                    "relevance_score": 7,
                    "signal_class": "infra_primitive",
                    "evidence": [f"https://github.com/x/i{index}"],
                }
            )
        selected = cloud_agent_runner.diversify_screening_candidates(candidates, 12)
        discussion_users = [
            cand
            for cand in selected
            if cand.get("signal_class") == "user_workflow"
            and cloud_agent_runner.is_social_only_evidence(cand)
        ]
        self.assertGreaterEqual(len(discussion_users), 3)

    def test_discussion_signal_count_and_warning(self) -> None:
        cloud_agent_runner.RUN_AUDIT["apply_warnings"] = []
        result = {
            "updates": [
                {
                    "path": "daily/2026-07.md",
                    "mode": "append",
                    "content": (
                        "## 2026-07-11\n\n### English\n\n"
                        "#### 2. New Signals\n\n"
                        "- Signal: vendor thing.\n"
                        "  - Why it matters: x.\n"
                        "  - Evidence strength: Strong.\n"
                        "  - Source: https://openai.com/news/a\n\n"
                        "#### 4. User Workflow & Field Notes\n\n"
                        "- Tool: agent loop.\n"
                        "  - Why it matters: y.\n"
                        "  - Evidence strength: Medium.\n"
                        "  - Source: https://www.reddit.com/r/ClaudeAI/comments/x/\n\n"
                        "- Tool: eval trick.\n"
                        "  - Why it matters: z.\n"
                        "  - Evidence strength: Medium.\n"
                        "  - Source: https://news.ycombinator.com/item?id=1\n"
                    ),
                }
            ]
        }
        cloud_agent_runner.audit_daily_depth(result)
        self.assertEqual(cloud_agent_runner.RUN_AUDIT["discussion_signal_count"], 2)
        self.assertTrue(
            any("Community share" in w for w in cloud_agent_runner.RUN_AUDIT["apply_warnings"])
        )

    def test_weekly_direction_notes_combines_assets(self) -> None:
        day = cloud_agent_runner.parse_date("2026-07-10")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "daily").mkdir(parents=True)
            (root / "radar.md").write_text(
                "## Open Questions\n\n- Will MCP win?\n", encoding="utf-8"
            )
            (root / "agent-watchlist.md").write_text(
                "## Old Agent\n\n- 2026-06-01\n", encoding="utf-8"
            )
            (root / "daily" / "2026-07.md").write_text(
                "## 2026-07-09\n\n- Signal: x.\n  - Claim audit: overreach; verify against source before trusting.\n",
                encoding="utf-8",
            )
            notes = cloud_agent_runner.weekly_direction_notes(root, day)
        self.assertIn("Open Questions Delta", notes)
        self.assertIn("Old Agent", notes)
        self.assertIn("Corroboration queue", notes)


if __name__ == "__main__":
    unittest.main()
