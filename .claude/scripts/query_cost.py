#!/usr/bin/env python3
"""
query_cost.py - Report token counts, estimated cost, and duration for Claude skill tasks.

Two modes:

  Default (last response only):
    python .claude/scripts/query_cost.py
    → reads the last assistant entry in the JSONL, reports its cost

  Task mode (whole task from start to finish):
    python .claude/scripts/query_cost.py --since <ISO-timestamp>
    → sums ALL assistant entries after the given timestamp, reports total cost + duration

  Stamp mode (write current time to stdout for use as --since value):
    python .claude/scripts/query_cost.py --stamp
    → prints the current UTC timestamp, e.g. 2026-03-11T14:23:01.456789

Typical skill workflow:
  1. Pre-flight:  START=$(python .claude/scripts/query_cost.py --stamp)
  2. ... do work ...
  3. End:         python .claude/scripts/query_cost.py --since "$START"

Output format (task mode):
  duration: 4m 32s | tokens: 32,131 in (31,730 cached + 401 live) / 399 out | cost: ~$0.0156  [N turns]

Output format (default mode):
  tokens: 32,131 in (31,730 cached + 401 live) / 399 out | cost: ~$0.0156

Pricing accounts for cache_read (10%) and cache_creation (25%) token rates,
which avoids 3-10x cost overcounting in long Claude Code sessions.
"""

import json
import os
import pathlib
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Pricing table — keys are substrings of model IDs
# ---------------------------------------------------------------------------
PRICING = {
    "sonnet-4-6": {"in": 3.00,  "cache_write": 0.75, "cache_read": 0.30, "out": 15.00},
    "opus-4":     {"in": 15.00, "cache_write": 3.75, "cache_read": 1.50, "out": 75.00},
    "haiku-4-5":  {"in": 0.80,  "cache_write": 0.20, "cache_read": 0.08, "out": 4.00},
}

# In task mode we need to scan from a timestamp — read up to 4MB to cover long tasks.
# In default mode we only need the last entry — 64KB is more than enough.
TAIL_SIZE_DEFAULT = 65536       # 64KB
TAIL_SIZE_TASK    = 4194304     # 4MB


def get_pricing(model_id: str) -> dict:
    """Match model ID substring to pricing tier. Returns zero-cost rates if unknown."""
    for key, rates in PRICING.items():
        if key in (model_id or ""):
            return rates
    return {"in": 0.0, "cache_write": 0.0, "cache_read": 0.0, "out": 0.0}


def parse_timestamp(ts: str) -> datetime:
    """Parse an ISO 8601 timestamp string into a UTC-aware datetime."""
    # Python 3.7+ fromisoformat doesn't handle trailing Z
    ts = ts.replace("Z", "+00:00")
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def find_project_dir() -> pathlib.Path | None:
    """Derive the Claude project directory from the current working directory."""
    cwd = os.getcwd()
    slug = cwd.lower().replace(":", "-").replace("\\", "-").replace("/", "-").strip("-")
    project_dir = pathlib.Path.home() / ".claude" / "projects" / slug
    return project_dir if project_dir.exists() else None


def find_active_jsonl(project_dir: pathlib.Path) -> pathlib.Path | None:
    """Return the most recently modified top-level JSONL file (not subagents)."""
    candidates = [f for f in project_dir.glob("*.jsonl") if f.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda f: f.stat().st_mtime)


def iter_tail_lines(jsonl_path: pathlib.Path, tail_size: int):
    """Yield lines from the tail of a JSONL file (most recent lines last)."""
    with open(jsonl_path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - tail_size))
        tail_bytes = f.read()
    tail_text = tail_bytes.decode("utf-8", errors="replace")
    return tail_text.strip().split("\n")


def collect_entries_since(jsonl_path: pathlib.Path, since: datetime) -> list[dict]:
    """
    Return all assistant entries with usage data whose timestamp >= since.
    Each entry includes model, usage, and timestamp for duration calculation.
    Scans up to TAIL_SIZE_TASK bytes from the end of the file.
    """
    lines = iter_tail_lines(jsonl_path, TAIL_SIZE_TASK)
    entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message", {})
        usage = msg.get("usage", {})
        if "output_tokens" not in usage:
            continue
        ts_str = obj.get("timestamp", "")
        if not ts_str:
            continue
        try:
            ts = parse_timestamp(ts_str)
        except (ValueError, TypeError):
            continue
        if ts >= since:
            entries.append({"model": msg.get("model", ""), "usage": usage, "ts": ts})
    return entries


def get_last_entry(jsonl_path: pathlib.Path) -> dict | None:
    """Return the most recent assistant entry with usage data (fast, 64KB tail)."""
    lines = iter_tail_lines(jsonl_path, TAIL_SIZE_DEFAULT)
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message", {})
        usage = msg.get("usage", {})
        if "output_tokens" not in usage:
            continue
        return {"model": msg.get("model", ""), "usage": usage}
    return None


def format_duration(seconds: float) -> str:
    """Format elapsed seconds as a human-readable duration string."""
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m {s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m {s:02d}s"


def compute_cost(entries: list[dict]) -> tuple[int, int, int, int, float]:
    """Sum token counts across entries and compute total cost. Returns (total_in, cached, live_write, output, cost)."""
    total_input_live = total_cache_write = total_cache_read = total_output = 0
    total_cost = 0.0
    M = 1_000_000

    for entry in entries:
        usage = entry["usage"]
        rates = get_pricing(entry["model"])

        input_live        = usage.get("input_tokens", 0)
        input_cache_write = usage.get("cache_creation_input_tokens", 0)
        input_cache_read  = usage.get("cache_read_input_tokens", 0)
        output            = usage.get("output_tokens", 0)

        total_input_live   += input_live
        total_cache_write  += input_cache_write
        total_cache_read   += input_cache_read
        total_output       += output
        total_cost += (
            (input_live        / M) * rates["in"] +
            (input_cache_write / M) * rates["cache_write"] +
            (input_cache_read  / M) * rates["cache_read"] +
            (output            / M) * rates["out"]
        )

    total_in = total_input_live + total_cache_write + total_cache_read
    live_and_write = total_input_live + total_cache_write
    return total_in, total_cache_read, live_and_write, total_output, total_cost


def main() -> None:
    args = sys.argv[1:]

    # --stamp mode: just print current UTC time for use as a --since value
    if "--stamp" in args:
        print(datetime.now(timezone.utc).isoformat())
        return

    # Parse --since <timestamp>
    since_dt = None
    if "--since" in args:
        idx = args.index("--since")
        if idx + 1 >= len(args):
            print("metrics: --since requires a timestamp argument")
            return
        try:
            since_dt = parse_timestamp(args[idx + 1])
        except (ValueError, TypeError):
            print(f"metrics: invalid timestamp '{args[idx + 1]}'")
            return

    # Locate project and JSONL
    project_dir = find_project_dir()
    if project_dir is None:
        print("metrics: project dir not found — cost unavailable")
        return

    jsonl_path = find_active_jsonl(project_dir)
    if jsonl_path is None:
        print("metrics: no JSONL session file found — cost unavailable")
        return

    # Collect entries
    if since_dt is not None:
        entries = collect_entries_since(jsonl_path, since_dt)
        if not entries:
            print("metrics: no assistant entries found after start timestamp — JSONL may not have flushed yet")
            return
        turns_label = f"  [{len(entries)} turn{'s' if len(entries) != 1 else ''}]"
        # Duration: from task start timestamp to last assistant response timestamp
        last_ts = max(e["ts"] for e in entries)
        elapsed = (last_ts - since_dt).total_seconds()
        duration_label = f"duration: {format_duration(elapsed)} | "
    else:
        entry = get_last_entry(jsonl_path)
        if entry is None:
            print("metrics: no assistant entry found — cost unavailable")
            return
        entries = [entry]
        turns_label = ""
        duration_label = ""

    total_in, cached, live_write, output, cost = compute_cost(entries)

    print(
        f"{duration_label}"
        f"tokens: {total_in:,} in "
        f"({cached:,} cached + {live_write:,} live) "
        f"/ {output:,} out | cost: ~${cost:.4f}"
        f"{turns_label}"
    )


if __name__ == "__main__":
    main()
