from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
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

    def test_run_log_and_source_health_are_written_by_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cloud_agent_runner.RUN_AUDIT["provider"] = "openrouter"
            cloud_agent_runner.RUN_AUDIT["models"] = ["deepseek/deepseek-v4-pro"]
            cloud_agent_runner.RUN_AUDIT["openrouter_calls"] = 1
            cloud_agent_runner.RUN_AUDIT["public_source_items"] = 3
            cloud_agent_runner.RUN_AUDIT["source_errors"] = ["feed:test: 404"]
            cloud_agent_runner.RUN_AUDIT["source_status"] = [{"name": "feed:test", "status": "error", "detail": "404"}]
            cloud_agent_runner.RUN_AUDIT["budget_status"] = "normal"
            day = cloud_agent_runner.parse_date("2026-07-02")
            cloud_agent_runner.append_run_log(root, "source-sweep", day, 2, "summary", ["source"])
            cloud_agent_runner.update_source_health(root, day)

            self.assertIn("OpenRouter calls attempted: 1", (root / "automation" / "runs" / "2026-07.md").read_text())
            self.assertIn("feed:test", (root / "automation" / "source-health.md").read_text())


if __name__ == "__main__":
    unittest.main()
