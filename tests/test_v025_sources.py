"""v0.25.0: source quality and per-day 中文 repair.

Each test pins one defect found in the September 2026 review: blanked CDATA
titles, navigation scraped as news, unfiltered HN, long-tail repos promoted to
release collectors, daily-only days skipping the lane shards, and a daily
中文 gate that pooled the whole month.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cloud_agent_runner = _load("cloud_agent_runner")
agent_radar = _load("agent_radar")
radar_bilingual = cloud_agent_runner.radar_bilingual
radar_collector_state = cloud_agent_runner.radar_collector_state


def _fake_response(body: str) -> mock.MagicMock:
    fake = mock.MagicMock()
    fake.read.return_value = body.encode("utf-8")
    fake.__enter__ = lambda s: fake
    fake.__exit__ = lambda *a: False
    return fake


class CdataTitleTest(unittest.TestCase):
    def test_strip_html_keeps_cdata_text(self) -> None:
        self.assertEqual(cloud_agent_runner.strip_html("<![CDATA[Introducing GPT-6]]>"), "Introducing GPT-6")
        self.assertEqual(
            cloud_agent_runner.strip_html("<![CDATA[<p>Agents &amp; <b>MCP</b></p>]]>"), "Agents & MCP"
        )

    def test_feed_items_carry_cdata_titles(self) -> None:
        rss = (
            "<rss><channel><item><title><![CDATA[Codex ships background agents]]></title>"
            "<link>https://openai.com/index/codex-bg</link></item></channel></rss>"
        )
        items: list[dict[str, str]] = []
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(rss)):
            cloud_agent_runner.collect_feed_items("https://openai.com/news/rss.xml", "openai-blog", 5, items, set())
        self.assertEqual(items[0]["title"], "Codex ships background agents")


class PageLinkFilterTest(unittest.TestCase):
    PAGE = (
        '<a href="#main">Skip to content</a>'
        '<a href="/contact-sales">Contact Sales</a>'
        '<a href="/products/sandboxes">Sandboxes</a>'
        '<a href="/">Acme home page link</a>'
        '<a href="https://other.example/x">Some external article</a>'
        '<a href="/blog/big-launch">Introducing Background Agents</a>'
        '<a href="/changelog/2-4">Cursor 2.4</a>'
        '<a href="/changelog/3-0#top">Cursor 3.0 ships agent mode</a>'
        '<a href="/security/update">Security update for the CLI sandbox escape</a>'
    )

    def test_navigation_is_dropped_and_section_links_come_first(self) -> None:
        links = cloud_agent_runner.page_link_candidates("https://cursor.com/changelog", self.PAGE)
        self.assertEqual(
            [url for _title, url in links],
            [
                "https://cursor.com/changelog/2-4",
                "https://cursor.com/changelog/3-0",
                "https://cursor.com/blog/big-launch",
                "https://cursor.com/security/update",
            ],
        )

    def test_navigation_no_longer_uses_up_the_item_limit(self) -> None:
        items: list[dict[str, str]] = []
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(self.PAGE)):
            cloud_agent_runner.collect_page_links("https://cursor.com/changelog", "cursor-changelog", 2, items, set())
        self.assertEqual([item["title"] for item in items], ["Cursor 2.4", "Cursor 3.0 ships agent mode"])


class TopicFilterTest(unittest.TestCase):
    def test_general_feed_keeps_only_agent_items(self) -> None:
        rss = "<rss><channel>" + "".join(
            f"<item><title>{title}</title><link>https://aws.amazon.com/{index}</link></item>"
            for index, title in enumerate(
                [
                    "Amazon EC2 R8i memory optimized instances in more regions",
                    "Amazon Bedrock AgentCore adds an MCP gateway",
                    "AWS DataSync launches a dashboard",
                    "Amazon Q Developer agent now runs tests",
                ]
            )
        ) + "</channel></rss>"
        items: list[dict[str, str]] = []
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(rss)):
            cloud_agent_runner.collect_feed_items("https://aws.example/feed", "aws-whats-new", 5, items, set())
        self.assertEqual(
            [item["title"] for item in items],
            ["Amazon Bedrock AgentCore adds an MCP gateway", "Amazon Q Developer agent now runs tests"],
        )

    def test_unlisted_feed_is_not_filtered(self) -> None:
        rss = "<rss><item><title>AWS DataSync launches a dashboard</title><link>https://a/1</link></item></rss>"
        items: list[dict[str, str]] = []
        with mock.patch("urllib.request.urlopen", return_value=_fake_response(rss)):
            cloud_agent_runner.collect_feed_items("https://a/feed", "aws-storage-blog", 5, items, set())
        self.assertEqual(len(items), 1)


class HackerNewsPointsTest(unittest.TestCase):
    def test_points_floor_is_requested_and_can_be_disabled(self) -> None:
        with mock.patch.object(cloud_agent_runner, "request_json", return_value={"hits": []}) as request_json:
            with mock.patch.dict(os.environ, {"HN_MIN_POINTS": ""}):
                cloud_agent_runner.collect_hn_items("coding agent", 5, [], set())
            self.assertIn("numericFilters=points%3E%3D10", request_json.call_args.args[0])
            with mock.patch.dict(os.environ, {"HN_MIN_POINTS": "0"}):
                cloud_agent_runner.collect_hn_items("coding agent", 5, [], set())
            self.assertNotIn("numericFilters", request_json.call_args.args[0])


class ReleaseRepoTest(unittest.TestCase):
    def test_context_repos_need_stars_and_research_log_is_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "agent-watchlist.md").write_text("https://github.com/big/agent\n", encoding="utf-8")
            (root / "sources.md").write_text(
                "https://github.com/tiny/brain\nhttps://github.com/mid/tool\n", encoding="utf-8"
            )
            (root / "research-log.md").write_text("https://github.com/log/only\n", encoding="utf-8")
            stars = {"big/agent": 5000, "tiny/brain": 3, "mid/tool": 250, "log/only": 99999}

            def meta(_root, repo):
                return {"stargazers_count": stars.get(repo, 10_000)}

            with mock.patch.object(cloud_agent_runner, "github_repo_meta", side_effect=meta), mock.patch.object(
                cloud_agent_runner, "DEFAULT_RELEASE_REPOS", ["openai/codex"]
            ), mock.patch.dict(os.environ, {"RELEASE_REPOS": "", "MIN_CONTEXT_REPO_STARS": ""}):
                repos = cloud_agent_runner.release_repos_from_context(root, 10)
        self.assertEqual(repos, ["openai/codex", "big/agent", "mid/tool"])

    def test_missing_star_count_does_not_qualify(self) -> None:
        self.assertFalse(cloud_agent_runner.context_repo_qualifies(None))
        self.assertFalse(cloud_agent_runner.context_repo_qualifies({}))

    def test_tags_are_only_fetched_when_a_repo_has_no_releases(self) -> None:
        calls: list[str] = []

        def fake(url, headers=None, timeout=10):
            calls.append(url)
            if "/releases" in url:
                return [] if "norel" in url else [{"name": "v1", "html_url": "https://github.com/a/b/releases/tag/v1"}]
            return [{"name": "v0.1", "commit": {"sha": "abc"}}]

        items: list[dict[str, str]] = []
        with mock.patch.object(cloud_agent_runner, "github_request_json", side_effect=fake):
            cloud_agent_runner.collect_github_releases("a/b", 2, items, set())
            cloud_agent_runner.collect_github_releases("a/norel", 2, items, set())
        self.assertEqual(sum("/tags" in url for url in calls), 1)
        self.assertEqual([item["source"] for item in items], ["github-release:a/b", "github-tag:a/norel"])


class AdvisoryCollectorTest(unittest.TestCase):
    def test_ghsa_items_are_official_lane(self) -> None:
        payload = [
            {
                "ghsa_id": "GHSA-xxxx-yyyy-zzzz",
                "summary": "MCP SDK path traversal",
                "html_url": "https://github.com/advisories/GHSA-xxxx-yyyy-zzzz",
                "severity": "high",
                "cve_id": "CVE-2026-1234",
                "vulnerabilities": [{"package": {"name": "@modelcontextprotocol/sdk"}}],
            }
        ]
        items: list[dict[str, str]] = []
        with mock.patch.object(cloud_agent_runner, "github_request_json", return_value=payload) as request:
            cloud_agent_runner.collect_github_advisories(5, items, set())
        self.assertIn("affects=mcp,fastmcp,@modelcontextprotocol/sdk", request.call_args.args[0])
        self.assertEqual(items[0]["title"], "GHSA-xxxx-yyyy-zzzz MCP SDK path traversal")
        self.assertIn("CVE-2026-1234", items[0]["note"])
        self.assertEqual(cloud_agent_runner.source_lane("ghsa"), "official")


class RedditOauthTest(unittest.TestCase):
    def test_api_lane_replaces_rss_only_with_credentials(self) -> None:
        with mock.patch.dict(os.environ, {"REDDIT_CLIENT_ID": "", "REDDIT_CLIENT_SECRET": ""}):
            self.assertFalse(cloud_agent_runner.collector_enabled("reddit-api"))
        with mock.patch.dict(os.environ, {"REDDIT_CLIENT_ID": "id", "REDDIT_CLIENT_SECRET": "secret"}):
            self.assertTrue(cloud_agent_runner.collector_enabled("reddit-api"))
        self.assertEqual(cloud_agent_runner.source_lane("reddit-api:ClaudeAI"), "reddit")

    def test_api_items_use_the_bearer_token(self) -> None:
        listing = {"data": {"children": [{"data": {"title": "Codex vs Claude Code", "permalink": "/r/x/comments/1/t/", "score": 40}}]}}
        with mock.patch.object(cloud_agent_runner, "reddit_oauth_token", return_value="tok"), mock.patch.object(
            cloud_agent_runner, "request_json", return_value=listing
        ) as request_json:
            items: list[dict[str, str]] = []
            cloud_agent_runner.collect_reddit_api_items("ClaudeAI", 3, items, set())
        self.assertEqual(request_json.call_args.kwargs["headers"]["Authorization"], "Bearer tok")
        self.assertEqual(items[0]["url"], "https://www.reddit.com/r/x/comments/1/t/")
        self.assertEqual(items[0]["source"], "reddit-api:ClaudeAI")


class RedirectTest(unittest.TestCase):
    def test_308_on_get_is_followed(self) -> None:
        handler = cloud_agent_runner.PermanentRedirectHandler()
        follow = handler.redirect_request(
            urllib.request.Request("https://e2b.dev/blog"), None, 308, "Permanent Redirect", {}, "https://e2b.dev/blog/"
        )
        self.assertEqual(follow.full_url, "https://e2b.dev/blog/")


class ScreeningShardCapTest(unittest.TestCase):
    def test_packages_shard_gets_a_smaller_window(self) -> None:
        self.assertEqual(cloud_agent_runner.screening_shard_cap("packages", 130), 45)
        self.assertEqual(cloud_agent_runner.screening_shard_cap("discussion", 130), 130)


class DailyOnlySharedScreeningTest(unittest.TestCase):
    def test_single_daily_task_uses_shared_collection_and_shards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            collection = ([], {}, [], 0)
            with mock.patch.object(cloud_agent_runner, "find_root", return_value=root), mock.patch.object(
                cloud_agent_runner, "ensure_report_shells"
            ), mock.patch.object(cloud_agent_runner, "model_provider", return_value="vercel-ai-gateway"), mock.patch.object(
                cloud_agent_runner, "task_uses_screening", return_value=True
            ), mock.patch.object(
                cloud_agent_runner, "prepare_shared_source_collection", return_value=collection
            ) as prepare, mock.patch.object(
                cloud_agent_runner, "preflight_shared_screening", return_value=("{}", 4)
            ) as preflight, mock.patch.object(cloud_agent_runner, "run_task") as run_task, mock.patch.dict(
                os.environ, {"PUBLIC_SOURCE_COLLECTION": "true", "SHARED_SCREENING": "true"}
            ):
                self.assertEqual(cloud_agent_runner.main(["--task", "daily", "--date", "2026-09-29"]), 0)
        prepare.assert_called_once()
        preflight.assert_called_once()
        self.assertEqual(run_task.call_args.kwargs["shared_screened"], "{}")
        self.assertEqual(run_task.call_args.kwargs["preflight_screen_calls"], 4)


def _english_day(label: str, signals: int = 6) -> str:
    sections = "".join(
        f"#### {index}. Section {index}\n\n- Signal {index}: vendor shipped feature {index} for coding agents. https://e.com/{index}\n\n"
        for index in range(1, signals + 1)
    )
    return f"## {label}\n\n### English\n\n{sections}"


def _chinese(count: int) -> str:
    return "".join(f"#### {index}. 小节\n\n- 第{index}条：厂商为编码代理发布了新功能，值得跟踪。\n\n" for index in range(1, count + 1))


def _day(label: str, chinese_bullets: int | None) -> str:
    block = _english_day(label)
    if chinese_bullets is not None:
        block += f"### 中文\n\n{_chinese(chinese_bullets)}"
    return block + "---\n\n"


class DailyChinesePerDayTest(unittest.TestCase):
    HEADER = "# Daily Agent Radar - 2026-09\n\n"

    def test_month_pooling_hid_a_thin_day(self) -> None:
        content = self.HEADER + _day("2026-09-02", 6) + _day("2026-09-03", None)
        # The whole-file check passes on the neighbour's Chinese...
        self.assertFalse(radar_bilingual.missing_chinese_substance(content))
        # ...the per-day check does not.
        self.assertEqual(radar_bilingual.thin_chinese_day_labels(content), ["2026-09-03"])

    def test_split_round_trips(self) -> None:
        content = self.HEADER + _day("2026-09-02", 6) + _day("2026-09-03", 2)
        self.assertEqual("".join(text for _label, text in radar_bilingual.split_daily_day_blocks(content)), content)

    def test_mirror_repairs_an_english_only_day(self) -> None:
        old = self.HEADER + _day("2026-09-02", 6)
        merged = old + _day("2026-09-03", None)
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=_chinese(6)) as mirror:
            out = cloud_agent_runner.repair_daily_chinese_blocks("daily/2026-09.md", old, merged)
        mirror.assert_called_once()
        self.assertEqual(mirror.call_args.args[0], "daily/2026-09.md ## 2026-09-03")
        self.assertEqual(radar_bilingual.thin_chinese_day_labels(out, include_marked=True), [])
        # The untouched earlier day is byte-identical.
        self.assertTrue(out.startswith(old))

    def test_failed_mirror_publishes_with_marker_instead_of_refusing(self) -> None:
        old = self.HEADER + _day("2026-09-02", 6)
        merged = old + _day("2026-09-03", 1)
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=""):
            out = cloud_agent_runner.repair_daily_chinese_blocks("daily/2026-09.md", old, merged)
        blocks = dict(radar_bilingual.split_daily_day_blocks(out))
        self.assertIn(radar_bilingual.CHINESE_MIRROR_DEGRADED_MARKER, blocks["2026-09-03"])
        self.assertNotIn(radar_bilingual.CHINESE_MIRROR_DEGRADED_MARKER, blocks["2026-09-02"])
        self.assertEqual(radar_bilingual.thin_chinese_day_labels(out), [])
        self.assertEqual(radar_bilingual.thin_chinese_day_labels(out, include_marked=True), ["2026-09-03"])

    def test_unchanged_thin_history_is_not_touched(self) -> None:
        old = self.HEADER + _day("2026-07-17", None)
        merged = old + _day("2026-07-18", 6)
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror") as mirror:
            out = cloud_agent_runner.repair_daily_chinese_blocks("daily/2026-07.md", old, merged)
        mirror.assert_not_called()
        self.assertEqual(out, merged)

    def test_stale_day_marker_is_cleared_when_the_day_is_rewritten_with_chinese(self) -> None:
        old = self.HEADER + _day("2026-09-03", 1)
        with mock.patch.object(cloud_agent_runner, "request_chinese_mirror", return_value=""):
            marked = cloud_agent_runner.repair_daily_chinese_blocks("daily/2026-09.md", self.HEADER, old)
        fixed = self.HEADER + _day("2026-09-03", 6)
        out = cloud_agent_runner.repair_daily_chinese_blocks("daily/2026-09.md", marked, fixed)
        self.assertNotIn(radar_bilingual.CHINESE_MIRROR_DEGRADED_MARKER, out)

    def test_validate_warns_per_day_without_failing_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "2026-07.md"
            path.write_text(self.HEADER + _day("2026-07-01", 6) + _day("2026-07-02", None), encoding="utf-8")
            errors, warnings = agent_radar.chinese_substance_findings(path, strict=True)
        self.assertEqual(errors, [])
        self.assertTrue(any("2026-07-02" in warning for warning in warnings))


class CollectStatusStaleTest(unittest.TestCase):
    def test_collectors_not_run_recently_are_stale_once_tracking_starts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state_path = root / "automation" / "collector-state.json"
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                json.dumps({"collectors": {"feed:old": {"status": "degraded"}}, "disabled": [], "rejected_repos": []}),
                encoding="utf-8",
            )
            payload = radar_collector_state.collect_status_payload(root)
            self.assertFalse(payload["collectors"][0]["stale"])  # no tracking yet
            radar_collector_state.record_result(root, "feed:new", True)
            rows = {row["name"]: row for row in radar_collector_state.collect_status_payload(root)["collectors"]}
        self.assertTrue(rows["feed:old"]["stale"])
        self.assertFalse(rows["feed:new"]["stale"])
        self.assertEqual(rows["feed:new"]["last_run"], dt.datetime.now(dt.timezone.utc).date().isoformat())


if __name__ == "__main__":
    unittest.main()


class GatewayFallbackChainTest(unittest.TestCase):
    """v0.26.0: routing by role, and a rejected fallback name does not end the chain."""

    def _ok(self) -> mock.MagicMock:
        good = mock.MagicMock()
        good.__enter__.return_value.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "{\"chinese_block\": \"- 中文\"}"}}]}
        ).encode("utf-8")
        return good

    def _http_error(self, code: int):
        import io
        import urllib.error

        return urllib.error.HTTPError("https://ai-gateway.vercel.sh", code, "err", {}, io.BytesIO(b"nope"))

    def _env(self, **extra: str) -> dict[str, str]:
        env = {"AI_GATEWAY_API_KEY": "x", "AI_GATEWAY_CALL_INTERVAL": "0", "AI_GATEWAY_429_ROUNDS": "2"}
        env.update(extra)
        return env

    def test_unknown_fallback_is_skipped_not_fatal(self) -> None:
        # primary 503 (transient) -> fallback-a 404 (unknown name) -> fallback-b ok.
        calls: list[str] = []

        def fake(request, timeout=0):
            model = json.loads(request.data)["model"]
            calls.append(model)
            if model == "primary":
                raise self._http_error(503)
            if model == "fallback-a":
                raise self._http_error(404)
            return self._ok()

        with mock.patch.dict(os.environ, self._env(AI_GATEWAY_FALLBACK_MODELS="fallback-a,fallback-b")), \
                mock.patch.object(urllib.request, "urlopen", side_effect=fake), \
                mock.patch.object(cloud_agent_runner.time, "sleep"):
            cloud_agent_runner.call_ai_gateway_model("p", "primary", role="synthesis")
        self.assertEqual(calls, ["primary", "fallback-a", "fallback-b"])

    def test_dead_model_is_not_retried_in_later_rounds(self) -> None:
        calls: list[str] = []

        def fake(request, timeout=0):
            model = json.loads(request.data)["model"]
            calls.append(model)
            if model == "fallback-a":
                raise self._http_error(404)
            if len(calls) < 4:
                raise self._http_error(503)
            return self._ok()

        with mock.patch.dict(os.environ, self._env(AI_GATEWAY_FALLBACK_MODELS="fallback-a")), \
                mock.patch.object(urllib.request, "urlopen", side_effect=fake), \
                mock.patch.object(cloud_agent_runner.time, "sleep"):
            with self.assertRaises(SystemExit):
                cloud_agent_runner.call_ai_gateway_model("p", "primary", role="synthesis")
        self.assertEqual(calls.count("fallback-a"), 1)

    def test_primary_client_error_still_stops_the_chain(self) -> None:
        # A 400 on the primary is about the payload; replaying it elsewhere won't help.
        calls: list[str] = []

        def fake(request, timeout=0):
            calls.append(json.loads(request.data)["model"])
            raise self._http_error(400)

        with mock.patch.dict(os.environ, self._env(AI_GATEWAY_FALLBACK_MODELS="fallback-a")), \
                mock.patch.object(urllib.request, "urlopen", side_effect=fake), \
                mock.patch.object(cloud_agent_runner.time, "sleep"):
            with self.assertRaises(SystemExit):
                cloud_agent_runner.call_ai_gateway_model("p", "primary", role="synthesis")
        self.assertEqual(calls, ["primary"])

    def test_chinese_mirror_uses_its_own_model_then_the_synthesis_model(self) -> None:
        calls: list[str] = []

        def fake(request, timeout=0):
            model = json.loads(request.data)["model"]
            calls.append(model)
            if model == "anthropic/claude-haiku-4.5":
                raise self._http_error(404)
            return self._ok()

        env = self._env(FINAL_SYNTHESIS_MODEL="openai/gpt-5-mini", CHINESE_MIRROR_MODEL="")
        with mock.patch.dict(os.environ, env), \
                mock.patch.object(cloud_agent_runner, "model_provider", return_value="vercel-ai-gateway"), \
                mock.patch.object(urllib.request, "urlopen", side_effect=fake), \
                mock.patch.object(cloud_agent_runner.time, "sleep"):
            block = cloud_agent_runner.request_chinese_mirror("daily/2026-10.md ## 2026-10-01", "- x", 3)
        self.assertEqual(calls, ["anthropic/claude-haiku-4.5", "openai/gpt-5-mini"])
        self.assertEqual(block, "- 中文")
