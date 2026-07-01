from __future__ import annotations

import importlib.util
import os
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
        self.assertIn("weekly", tasks)
        self.assertIn("promote-candidates", tasks)

    def test_public_source_collection_can_be_disabled(self) -> None:
        with mock.patch.dict(os.environ, {"PUBLIC_SOURCE_COLLECTION": "false"}, clear=True):
            self.assertIn("disabled", cloud_agent_runner.collect_public_sources("daily"))

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


if __name__ == "__main__":
    unittest.main()
