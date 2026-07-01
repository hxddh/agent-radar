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


if __name__ == "__main__":
    unittest.main()
