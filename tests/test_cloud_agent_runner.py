from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "cloud_agent_runner.py"


spec = importlib.util.spec_from_file_location("cloud_agent_runner", MODULE_PATH)
assert spec is not None
cloud_agent_runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cloud_agent_runner)


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
            self.assertEqual(cloud_agent_runner.public_source_budget("daily"), 80)
            self.assertEqual(cloud_agent_runner.public_source_budget("source-sweep"), 120)
            self.assertEqual(cloud_agent_runner.public_source_budget("weekly"), 120)
            self.assertEqual(cloud_agent_runner.public_source_budget("monthly"), 160)
            self.assertGreaterEqual(cloud_agent_runner.MAX_PUBLIC_SOURCE_ITEMS, 200)

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
        prompt = cloud_agent_runner.build_prompt(
            "daily",
            cloud_agent_runner.parse_date("2026-07-02"),
            ["research-log.md"],
            "repo context",
            "public source snapshot",
        )
        self.assertIn("do not use paid search tools", prompt)
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

    def test_pypi_enabled_by_default(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertTrue(cloud_agent_runner.collector_enabled("pypi"))

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


if __name__ == "__main__":
    unittest.main()
