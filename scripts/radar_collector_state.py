#!/usr/bin/env python3
"""Persistent collector health state for Agent Radar."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


STATE_PATH = Path("automation/collector-state.json")
DEFAULT_DISABLE_AFTER_ERRORS = 3


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


def is_disabled(root: Path, collector_name: str) -> bool:
    state = load_state(root)
    disabled = set(state.get("disabled", [])) | env_disabled_collectors()
    return collector_name in disabled


def record_result(root: Path, collector_name: str, ok: bool, detail: str = "") -> None:
    state = load_state(root)
    collectors = state.setdefault("collectors", {})
    record = collectors.setdefault(
        collector_name,
        {"ok": 0, "error": 0, "last_status": "", "last_detail": ""},
    )
    if ok:
        record["ok"] = int(record.get("ok", 0)) + 1
        record["last_status"] = "ok"
    else:
        record["error"] = int(record.get("error", 0)) + 1
        record["last_status"] = "error"
        record["last_detail"] = detail[:220]
        threshold = DEFAULT_DISABLE_AFTER_ERRORS
        if int(record["error"]) >= threshold and int(record.get("ok", 0)) == 0:
            disabled = set(state.get("disabled", []))
            disabled.add(collector_name)
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
    for prefix in ("release", "tag"):
        name = f"{prefix}:{repo}"
        disabled = set(state.get("disabled", []))
        disabled.add(name)
        state["disabled"] = sorted(disabled)
        collectors.setdefault(
            name,
            {"ok": 0, "error": 0, "last_status": "rejected", "last_detail": reason[:220]},
        )
    save_state(root, state)


def active_collectors(root: Path, names: list[str]) -> list[str]:
    state = load_state(root)
    disabled = set(state.get("disabled", [])) | env_disabled_collectors()
    return [name for name in names if name not in disabled]
