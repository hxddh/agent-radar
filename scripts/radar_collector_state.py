#!/usr/bin/env python3
"""Persistent collector health state for Agent Radar."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_PATH = Path("automation/collector-state.json")
DEFAULT_DISABLE_AFTER_ERRORS = 3
DEFAULT_RECOVER_AFTER_OK = 3
DEFAULT_DEGRADED_DISABLE_RUNS = 7
TRANSIENT_ERROR_MARKERS = ("429", "timeout", "503", "502", "504", "500", "timed out")
PERMANENT_ERROR_MARKERS = ("404", "410")


def load_state(root: Path) -> dict[str, Any]:
    path = root / STATE_PATH
    if not path.exists():
        return {"collectors": {}, "disabled": [], "rejected_repos": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"collectors": {}, "disabled": [], "rejected_repos": []}
    if not isinstance(data, dict):
        return {"collectors": {}, "disabled": [], "rejected_repos": []}
    data.setdefault("collectors", {})
    data.setdefault("disabled", [])
    data.setdefault("rejected_repos", [])
    return data


def save_state(root: Path, state: dict[str, Any]) -> None:
    path = root / STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def env_disabled_collectors() -> set[str]:
    value = os.environ.get("DISABLED_COLLECTORS", "")
    if not value.strip():
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def error_class(collector_name: str, detail: str) -> str:
    text = detail.lower()
    if any(marker in detail for marker in PERMANENT_ERROR_MARKERS):
        return "permanent"
    if "403" in detail and collector_name.startswith(("reddit", "page:", "feed:")):
        return "permanent"
    if any(marker in text for marker in TRANSIENT_ERROR_MARKERS):
        return "transient"
    return "transient"


def collector_record(state: dict[str, Any], collector_name: str) -> dict[str, Any]:
    collectors = state.setdefault("collectors", {})
    record = collectors.setdefault(
        collector_name,
        {
            "ok": 0,
            "error": 0,
            "last_status": "",
            "last_detail": "",
            "status": "ok",
            "degraded_runs": 0,
            "ok_streak": 0,
            "next_retry_after": "",
        },
    )
    record.setdefault("status", "ok")
    record.setdefault("degraded_runs", 0)
    record.setdefault("ok_streak", 0)
    record.setdefault("next_retry_after", "")
    return record


def is_disabled(root: Path, collector_name: str) -> bool:
    state = load_state(root)
    disabled = set(state.get("disabled", [])) | env_disabled_collectors()
    if collector_name in disabled:
        return True
    record = state.get("collectors", {}).get(collector_name, {})
    if record.get("status") == "disabled":
        return True
    retry_after = str(record.get("next_retry_after", ""))
    if record.get("status") == "degraded" and retry_after:
        try:
            if retry_after > utc_now_iso():
                return True
        except TypeError:
            pass
    return False


def record_result(root: Path, collector_name: str, ok: bool, detail: str = "") -> None:
    state = load_state(root)
    record = collector_record(state, collector_name)
    if ok:
        record["ok"] = int(record.get("ok", 0)) + 1
        record["last_status"] = "ok"
        record["last_detail"] = ""
        record["ok_streak"] = int(record.get("ok_streak", 0)) + 1
        record["next_retry_after"] = ""
        if record.get("status") == "degraded" and int(record.get("ok_streak", 0)) >= DEFAULT_RECOVER_AFTER_OK:
            record["status"] = "ok"
            record["degraded_runs"] = 0
    else:
        record["error"] = int(record.get("error", 0)) + 1
        record["last_status"] = "error"
        record["last_detail"] = detail[:220]
        record["ok_streak"] = 0
        kind = error_class(collector_name, detail)
        disabled = set(state.get("disabled", []))
        if kind == "permanent":
            if int(record.get("error", 0)) >= DEFAULT_DISABLE_AFTER_ERRORS and int(record.get("ok", 0)) == 0:
                disabled.add(collector_name)
                record["status"] = "disabled"
        else:
            record["status"] = "degraded"
            record["degraded_runs"] = int(record.get("degraded_runs", 0)) + 1
            backoff_minutes = min(60, 2 ** min(int(record.get("degraded_runs", 1)), 5))
            retry = datetime.now(timezone.utc).timestamp() + backoff_minutes * 60
            record["next_retry_after"] = (
                datetime.fromtimestamp(retry, tz=timezone.utc).replace(microsecond=0).isoformat()
            )
            if int(record.get("degraded_runs", 0)) >= DEFAULT_DEGRADED_DISABLE_RUNS:
                disabled.add(collector_name)
                record["status"] = "disabled"
        state["disabled"] = sorted(disabled)
        if "404" in detail and collector_name.startswith(("release:", "tag:")):
            repo = collector_name.split(":", 1)[1]
            record_repo_rejection(root, repo, detail, state=state)
    save_state(root, state)


def rejected_repos(root: Path) -> set[str]:
    state = load_state(root)
    repos = state.get("rejected_repos", [])
    if not isinstance(repos, list):
        return set()
    return {str(item) for item in repos}


def record_repo_rejection(
    root: Path,
    repo: str,
    reason: str = "",
    state: dict[str, Any] | None = None,
) -> None:
    if state is None:
        state = load_state(root)
    rejected = set(state.get("rejected_repos", []))
    rejected.add(repo)
    state["rejected_repos"] = sorted(rejected)
    collectors = state.setdefault("collectors", {})
    disabled = set(state.get("disabled", []))
    for prefix in ("release", "tag"):
        name = f"{prefix}:{repo}"
        disabled.add(name)
        collectors.setdefault(
            name,
            {
                "ok": 0,
                "error": 0,
                "last_status": "rejected",
                "last_detail": reason[:220],
                "status": "disabled",
                "degraded_runs": 0,
                "ok_streak": 0,
                "next_retry_after": "",
            },
        )
    state["disabled"] = sorted(disabled)
    save_state(root, state)


def active_collectors(root: Path, names: list[str]) -> list[str]:
    return [name for name in names if not is_disabled(root, name)]


def lane_health_scores(lane_stats: dict[str, dict[str, Any]]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for lane, stats in lane_stats.items():
        ok = int(stats.get("ok", 0))
        err = int(stats.get("error", 0))
        total = ok + err
        if total == 0:
            scores[lane] = 0.5
        else:
            scores[lane] = ok / total
    return scores


def collect_status_payload(root: Path) -> dict[str, Any]:
    state = load_state(root)
    collectors = state.get("collectors", {})
    rows: list[dict[str, Any]] = []
    for name in sorted(collectors):
        record = collectors[name]
        if not isinstance(record, dict):
            continue
        rows.append(
            {
                "name": name,
                "ok": int(record.get("ok", 0)),
                "error": int(record.get("error", 0)),
                "status": record.get("status", "ok"),
                "last_detail": record.get("last_detail", ""),
                "next_retry_after": record.get("next_retry_after", ""),
                "disabled": name in set(state.get("disabled", [])) | env_disabled_collectors(),
            }
        )
    return {
        "disabled_count": len(set(state.get("disabled", [])) | env_disabled_collectors()),
        "rejected_repos": list(state.get("rejected_repos", [])),
        "collectors": rows,
    }


def fallback_feed_for_collector(collector_name: str) -> tuple[str, str] | None:
    """Optional RSS fallback when a page collector is disabled."""
    fallbacks = {
        "page:anthropic-news": ("feed:anthropic-news", "https://www.anthropic.com/news/rss.xml"),
        "page:cursor-changelog": ("feed:cursor-changelog", "https://cursor.com/changelog/rss.xml"),
    }
    return fallbacks.get(collector_name)
