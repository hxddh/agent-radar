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
# Even hard-disabled collectors are retried after this window so a temporary
# outage (a repo rename, a rate-limit spell) is not a permanent death sentence.
HARD_DISABLE_RETRY_MINUTES = 1440
TRANSIENT_ERROR_MARKERS = ("429", "timeout", "503", "502", "504", "500", "timed out")
PERMANENT_ERROR_MARKERS = ("404", "410")


def _empty_state() -> dict[str, Any]:
    return {"collectors": {}, "disabled": [], "rejected_repos": []}


def load_state(root: Path) -> dict[str, Any]:
    path = root / STATE_PATH
    backup = path.with_name(path.name + ".bak")
    # Fall back to the last good backup if the primary file was truncated by an
    # interrupted write, so one killed run cannot silently erase all history.
    for candidate in (path, backup):
        if not candidate.exists():
            continue
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        data.setdefault("collectors", {})
        data.setdefault("disabled", [])
        data.setdefault("rejected_repos", [])
        return data
    return _empty_state()


def save_state(root: Path, state: dict[str, Any]) -> None:
    path = root / STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    # Keep the previous good copy as a backup, then swap the new file in
    # atomically so a crash mid-write leaves either the old or the new file,
    # never a truncated one.
    if path.exists():
        try:
            path.with_name(path.name + ".bak").write_text(
                path.read_text(encoding="utf-8"), encoding="utf-8"
            )
        except OSError:
            pass
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    os.replace(tmp, path)


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
            "permanent_streak": 0,
            "ok_streak": 0,
            "next_retry_after": "",
        },
    )
    record.setdefault("status", "ok")
    record.setdefault("degraded_runs", 0)
    record.setdefault("permanent_streak", 0)
    record.setdefault("ok_streak", 0)
    record.setdefault("next_retry_after", "")
    return record


def _backoff_iso(runs: int, minutes: int | None = None) -> str:
    if minutes is None:
        # 2**6 == 64 so the 60-minute ceiling is actually reachable.
        minutes = min(60, 2 ** min(max(runs, 1), 6))
    retry = datetime.now(timezone.utc).timestamp() + minutes * 60
    return datetime.fromtimestamp(retry, tz=timezone.utc).replace(microsecond=0).isoformat()


def is_disabled(root: Path, collector_name: str) -> bool:
    if collector_name in env_disabled_collectors():
        return True
    state = load_state(root)
    record = state.get("collectors", {}).get(collector_name, {})
    retry_after = str(record.get("next_retry_after", ""))
    hard_disabled = collector_name in set(state.get("disabled", [])) or record.get("status") == "disabled"
    now = utc_now_iso()
    if hard_disabled:
        # Honor the retry window so a hard-disabled collector gets one more
        # chance once the window passes; an empty window stays disabled.
        if retry_after and retry_after <= now:
            return False
        return True
    if record.get("status") == "degraded" and retry_after and retry_after > now:
        return True
    return False


def record_result(root: Path, collector_name: str, ok: bool, detail: str = "") -> None:
    state = load_state(root)
    record = collector_record(state, collector_name)
    disabled = set(state.get("disabled", []))
    if ok:
        record["ok"] = int(record.get("ok", 0)) + 1
        record["last_status"] = "ok"
        record["last_detail"] = ""
        record["ok_streak"] = int(record.get("ok_streak", 0)) + 1
        record["permanent_streak"] = 0
        record["degraded_runs"] = 0
        record["next_retry_after"] = ""
        if record.get("status") in ("degraded", "disabled"):
            # A single success proves the collector works again: lift the hard
            # disable and let the status settle back to ok after a short streak.
            disabled.discard(collector_name)
            if int(record.get("ok_streak", 0)) >= DEFAULT_RECOVER_AFTER_OK:
                record["status"] = "ok"
            else:
                record["status"] = "degraded"
        # Recover a rejected repo when either of its collectors succeeds.
        if collector_name.startswith(("release:", "tag:")):
            _recover_repo(state, collector_name.split(":", 1)[1], disabled)
        state["disabled"] = sorted(disabled)
    else:
        record["error"] = int(record.get("error", 0)) + 1
        record["last_status"] = "error"
        record["last_detail"] = detail[:220]
        record["ok_streak"] = 0
        kind = error_class(collector_name, detail)
        if kind == "permanent":
            record["permanent_streak"] = int(record.get("permanent_streak", 0)) + 1
            record["degraded_runs"] = int(record.get("degraded_runs", 0)) + 1
            record["next_retry_after"] = _backoff_iso(int(record.get("degraded_runs", 1)))
            record["status"] = "degraded"
            # Disable after repeated permanent failures with no intervening
            # success (a genuinely gone resource), not on a single transient 404.
            if int(record.get("permanent_streak", 0)) >= DEFAULT_DISABLE_AFTER_ERRORS:
                disabled.add(collector_name)
                record["status"] = "disabled"
                record["next_retry_after"] = _backoff_iso(0, HARD_DISABLE_RETRY_MINUTES)
                if "404" in detail and collector_name.startswith(("release:", "tag:")):
                    repo = collector_name.split(":", 1)[1]
                    state["disabled"] = sorted(disabled)
                    record_repo_rejection(root, repo, detail, state=state)
                    disabled = set(state.get("disabled", []))
        else:
            record["permanent_streak"] = 0
            record["status"] = "degraded"
            record["degraded_runs"] = int(record.get("degraded_runs", 0)) + 1
            record["next_retry_after"] = _backoff_iso(int(record.get("degraded_runs", 1)))
            if int(record.get("degraded_runs", 0)) >= DEFAULT_DEGRADED_DISABLE_RUNS:
                disabled.add(collector_name)
                record["status"] = "disabled"
                record["next_retry_after"] = _backoff_iso(0, HARD_DISABLE_RETRY_MINUTES)
        state["disabled"] = sorted(disabled)
    save_state(root, state)


def _recover_repo(state: dict[str, Any], repo: str, disabled: set[str]) -> None:
    rejected = set(state.get("rejected_repos", []))
    if repo in rejected:
        rejected.discard(repo)
        state["rejected_repos"] = sorted(rejected)
    collectors = state.setdefault("collectors", {})
    for prefix in ("release", "tag"):
        name = f"{prefix}:{repo}"
        disabled.discard(name)
        rec = collectors.get(name)
        if isinstance(rec, dict) and rec.get("status") == "disabled":
            rec["status"] = "degraded"
            rec["next_retry_after"] = ""


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
    disabled = set(state.get("disabled", []))
    retry_after = _backoff_iso(0, HARD_DISABLE_RETRY_MINUTES)
    for prefix in ("release", "tag"):
        name = f"{prefix}:{repo}"
        disabled.add(name)
        # Update existing records too, so status never contradicts the disabled
        # list (a stale "ok"/"degraded" row while the name sits in disabled).
        record = collector_record(state, name)
        record["last_status"] = "rejected"
        record["last_detail"] = reason[:220]
        record["status"] = "disabled"
        record["next_retry_after"] = retry_after
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
