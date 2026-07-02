#!/usr/bin/env python3
"""Persistent collector health state for Agent Radar."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STATE_PATH = Path("automation/collector-state.json")
DEFAULT_DISABLE_AFTER_ERRORS = 3


def load_state(root: Path) -> dict[str, Any]:
    path = root / STATE_PATH
    if not path.exists():
        return {"collectors": {}, "disabled": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"collectors": {}, "disabled": []}
    if not isinstance(data, dict):
        return {"collectors": {}, "disabled": []}
    data.setdefault("collectors", {})
    data.setdefault("disabled", [])
    return data


def save_state(root: Path, state: dict[str, Any]) -> None:
    path = root / STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def is_disabled(root: Path, collector_name: str) -> bool:
    state = load_state(root)
    return collector_name in state.get("disabled", [])


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
    save_state(root, state)


def active_collectors(root: Path, names: list[str]) -> list[str]:
    state = load_state(root)
    disabled = set(state.get("disabled", []))
    return [name for name in names if name not in disabled]
