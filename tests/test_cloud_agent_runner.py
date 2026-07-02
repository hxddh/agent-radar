from __future__ import annotations

import importlib.util
import os
import tempfile
import time
import unittest
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
                ["z-ai/glm-5.2"],
            )
            self.assertEqual(
                cloud_agent_runner.openrouter_models_for_task("monthly"),
                ["z-ai/glm-5.2"],
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
        self.assertIn("Treat this task as discovery, not promotion.", prompt)
        self.assertIn("Do not update agent-watchlist.md", prompt)
        self.assertIn("daily/weekly/monthly runs may promote it automatically", prompt)

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
        self.assertIn("Promote automatically; do not ask for human confirmation.", prompt)
        self.assertIn("Promote at most 3 candidates per run.", prompt)

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

    def test_shared_screening_reuses_cached_screen_text(self) -> None:
        screen_cache: dict[str, str] = {"text": '{"summary":"cached-screen"}'}
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
                                    shared_collection=([], {}, []),
                                    screen_cache=screen_cache,
                                )
        invoke_mock.assert_called_once()
        self.assertEqual(invoke_mock.call_args.kwargs.get("shared_screened"), '{"summary":"cached-screen"}')
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


if __name__ == "__main__":
    unittest.main()
