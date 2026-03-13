#!/usr/bin/env python3
"""
query_cost.py - Report token counts, estimated cost, and duration for motion skill tasks.

Supports both local Claude project logs and local Codex session logs.

Modes:

  Default (last response / last token update):
    python .claude/scripts/query_cost.py

  Latest finished query:
    python .claude/scripts/query_cost.py --latest-query

  Task mode (from a start timestamp):
    python .claude/scripts/query_cost.py --since <ISO-timestamp>

  Stamp mode:
    python .claude/scripts/query_cost.py --stamp

Optional controls:
  --source auto|claude|codex
  --budget motion-build-single|motion-build-page|motion-upgrade-single
  --list-budgets

Output format:
  duration: 4m 32s | tokens: 32,131 in (31,730 cached + 401 live) / 399 out | estimated cost: ~$0.0156  [N requests]
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
from dataclasses import dataclass
from datetime import datetime, timezone


CODEX_TAIL_MATCH = 524288

CLAUDE_PRICING = {
    "sonnet-4-6": {"in": 3.00, "cache_write": 0.75, "cache_read": 0.30, "out": 15.00},
    "opus-4": {"in": 15.00, "cache_write": 3.75, "cache_read": 1.50, "out": 75.00},
    "haiku-4-5": {"in": 0.80, "cache_write": 0.20, "cache_read": 0.08, "out": 4.00},
}

OPENAI_PRICING = [
    ("gpt-5.4-pro", {"in": 30.00, "cache_write": 0.0, "cache_read": 0.0, "out": 180.00}),
    ("gpt-5.2-pro", {"in": 21.00, "cache_write": 0.0, "cache_read": 0.0, "out": 168.00}),
    ("gpt-5.4", {"in": 2.50, "cache_write": 0.0, "cache_read": 0.25, "out": 15.00}),
    ("gpt-5.3-codex", {"in": 1.75, "cache_write": 0.0, "cache_read": 0.175, "out": 14.00}),
    ("gpt-5.2-codex", {"in": 1.75, "cache_write": 0.0, "cache_read": 0.175, "out": 14.00}),
    ("gpt-5.2-chat-latest", {"in": 1.75, "cache_write": 0.0, "cache_read": 0.175, "out": 14.00}),
    ("gpt-5.2", {"in": 1.75, "cache_write": 0.0, "cache_read": 0.175, "out": 14.00}),
    ("gpt-5.1-codex-max", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5.1-codex", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5-codex", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5.1-chat-latest", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5-chat-latest", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5.1", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5", {"in": 1.25, "cache_write": 0.0, "cache_read": 0.125, "out": 10.00}),
    ("gpt-5-mini", {"in": 0.25, "cache_write": 0.0, "cache_read": 0.025, "out": 2.00}),
    ("gpt-5-mini-latest", {"in": 0.25, "cache_write": 0.0, "cache_read": 0.025, "out": 2.00}),
    ("gpt-5-nano", {"in": 0.05, "cache_write": 0.0, "cache_read": 0.005, "out": 0.40}),
]

BUDGETS = {
    "motion-build-single": {
        "label": "simple single-element motion-build",
        "live_max": 2500,
        "out_max": 1800,
    },
    "motion-build-page": {
        "label": "page-level motion-build",
        "live_max": 5500,
        "out_max": 3500,
    },
    "motion-upgrade-single": {
        "label": "simple single-file motion-upgrade",
        "live_max": 6000,
        "out_max": 2500,
    },
}


@dataclass
class CostEntry:
    model: str
    live_input: int
    cache_write_input: int
    cache_read_input: int
    output: int


@dataclass
class ClaudeSource:
    jsonl_path: pathlib.Path


@dataclass
class CodexSample:
    ts: datetime
    model: str
    total_input: int
    total_cached: int
    total_output: int
    last_input: int
    last_cached: int
    last_output: int


@dataclass
class CodexSource:
    jsonl_path: pathlib.Path
    samples: list[CodexSample]
    events: list["CodexEvent"]
    turn_timestamps: list[datetime]


@dataclass
class ClaudeNode:
    uuid: str
    parent_uuid: str | None
    ts: datetime
    entry_type: str
    prompt_id: str | None
    source_tool_assistant_uuid: str | None
    tool_use_result: bool
    request_id: str | None
    model: str
    usage: dict | None


@dataclass
class CodexEvent:
    ts: datetime
    kind: str
    sample_index: int | None = None


@dataclass
class QueryWindow:
    entries: list[CostEntry]
    start_ts: datetime
    end_ts: datetime
    request_count: int


def parse_timestamp(ts: str) -> datetime:
    ts = ts.replace("Z", "+00:00")
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def normalize_path(value: str) -> str:
    return os.path.normcase(os.path.normpath(value))


def get_pricing(model_id: str) -> tuple[dict, bool]:
    model = (model_id or "").lower()
    for key, rates in CLAUDE_PRICING.items():
        if key in model:
            return rates, True
    for key, rates in OPENAI_PRICING:
        if key in model:
            return rates, True
    return {"in": 0.0, "cache_write": 0.0, "cache_read": 0.0, "out": 0.0}, False


def iter_tail_lines(jsonl_path: pathlib.Path, tail_size: int) -> list[str]:
    with open(jsonl_path, "rb") as handle:
        handle.seek(0, 2)
        size = handle.tell()
        handle.seek(max(0, size - tail_size))
        tail_bytes = handle.read()
    return tail_bytes.decode("utf-8", errors="replace").strip().split("\n")


def format_duration(seconds: float) -> str:
    whole = int(seconds)
    if whole < 60:
        return f"{whole}s"
    minutes, seconds_part = divmod(whole, 60)
    if minutes < 60:
        return f"{minutes}m {seconds_part:02d}s"
    hours, minutes_part = divmod(minutes, 60)
    return f"{hours}h {minutes_part:02d}m {seconds_part:02d}s"


def find_claude_source(cwd: str) -> ClaudeSource | None:
    slug = cwd.lower().replace(":", "-").replace("\\", "-").replace("/", "-").strip("-")
    project_dir = pathlib.Path.home() / ".claude" / "projects" / slug
    if not project_dir.exists():
        return None
    candidates = [path for path in project_dir.glob("*.jsonl") if path.is_file()]
    if not candidates:
        return None
    return ClaudeSource(max(candidates, key=lambda path: path.stat().st_mtime))


def file_matches_cwd(path: pathlib.Path, cwd_norm: str) -> bool:
    for line in reversed(iter_tail_lines(path, CODEX_TAIL_MATCH)):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "turn_context":
            continue
        payload = obj.get("payload", {})
        if normalize_path(payload.get("cwd", "")) == cwd_norm:
            return True
    return False


def iter_codex_candidates() -> list[pathlib.Path]:
    codex_root = pathlib.Path.home() / ".codex"
    candidates: list[pathlib.Path] = []
    archived = codex_root / "archived_sessions"
    sessions = codex_root / "sessions"
    if archived.exists():
        candidates.extend(path for path in archived.glob("*.jsonl") if path.is_file())
    if sessions.exists():
        candidates.extend(path for path in sessions.rglob("*.jsonl") if path.is_file())
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)


def load_codex_source(cwd: str) -> CodexSource | None:
    cwd_norm = normalize_path(cwd)
    selected: pathlib.Path | None = None
    for candidate in iter_codex_candidates():
        if file_matches_cwd(candidate, cwd_norm):
            selected = candidate
            break
    if selected is None:
        return None

    samples: list[CodexSample] = []
    events: list[CodexEvent] = []
    turn_timestamps: list[datetime] = []
    current_model = ""
    previous_totals: tuple[int, int, int] | None = None

    for raw_line in selected.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw_line.strip():
            continue
        try:
            obj = json.loads(raw_line)
        except json.JSONDecodeError:
            continue

        obj_type = obj.get("type")
        if obj_type == "turn_context":
            payload = obj.get("payload", {})
            if normalize_path(payload.get("cwd", "")) == cwd_norm:
                current_model = payload.get("model", current_model)
                try:
                    turn_timestamps.append(parse_timestamp(obj.get("timestamp", "")))
                except (TypeError, ValueError):
                    pass
            continue

        if obj_type != "event_msg":
            continue
        payload = obj.get("payload", {})
        event_type = payload.get("type")
        try:
            ts = parse_timestamp(obj.get("timestamp", ""))
        except (TypeError, ValueError):
            continue
        if event_type != "token_count":
            if event_type in {"task_started", "task_complete", "turn_aborted", "user_message"}:
                events.append(CodexEvent(ts=ts, kind=event_type))
            continue

        info = payload.get("info", {})
        total = info.get("total_token_usage", {})
        last = info.get("last_token_usage", {})
        if not total or "input_tokens" not in total or "output_tokens" not in total:
            continue

        totals = (
            int(total.get("input_tokens", 0)),
            int(total.get("cached_input_tokens", 0)),
            int(total.get("output_tokens", 0)),
        )
        if previous_totals == totals:
            continue
        previous_totals = totals
        samples.append(
            CodexSample(
                ts=ts,
                model=current_model,
                total_input=totals[0],
                total_cached=totals[1],
                total_output=totals[2],
                last_input=int(last.get("input_tokens", 0)),
                last_cached=int(last.get("cached_input_tokens", 0)),
                last_output=int(last.get("output_tokens", 0)),
            )
        )
        events.append(CodexEvent(ts=ts, kind="token_count", sample_index=len(samples) - 1))

    if not samples:
        return None
    return CodexSource(selected, samples, events, turn_timestamps)


def choose_source(cwd: str, source: str) -> tuple[str, ClaudeSource | CodexSource] | tuple[None, None]:
    if source == "claude":
        chosen = find_claude_source(cwd)
        return ("claude", chosen) if chosen else (None, None)
    if source == "codex":
        chosen = load_codex_source(cwd)
        return ("codex", chosen) if chosen else (None, None)

    claude_source = find_claude_source(cwd)
    codex_source = load_codex_source(cwd)
    candidates: list[tuple[str, pathlib.Path, ClaudeSource | CodexSource]] = []
    if claude_source is not None:
        candidates.append(("claude", claude_source.jsonl_path, claude_source))
    if codex_source is not None:
        candidates.append(("codex", codex_source.jsonl_path, codex_source))
    if not candidates:
        return None, None
    selected = max(candidates, key=lambda item: item[1].stat().st_mtime)
    return selected[0], selected[2]


def load_claude_nodes(jsonl_path: pathlib.Path) -> tuple[dict[str, ClaudeNode], list[ClaudeNode]]:
    nodes: dict[str, ClaudeNode] = {}
    assistant_requests: dict[str, ClaudeNode] = {}
    for line in jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        entry_type = obj.get("type")
        if entry_type not in {"user", "assistant"}:
            continue
        uuid = obj.get("uuid")
        timestamp = obj.get("timestamp", "")
        if not uuid or not timestamp:
            continue
        try:
            ts = parse_timestamp(timestamp)
        except (TypeError, ValueError):
            continue
        message = obj.get("message", {})
        usage = message.get("usage") if isinstance(message, dict) else None
        node = ClaudeNode(
            uuid=uuid,
            parent_uuid=obj.get("parentUuid"),
            ts=ts,
            entry_type=entry_type,
            prompt_id=obj.get("promptId"),
            source_tool_assistant_uuid=obj.get("sourceToolAssistantUUID"),
            tool_use_result=bool(obj.get("toolUseResult")),
            request_id=obj.get("requestId"),
            model=message.get("model", "") if isinstance(message, dict) else "",
            usage=usage if isinstance(usage, dict) else None,
        )
        nodes[uuid] = node
        if node.entry_type != "assistant" or not node.usage or "output_tokens" not in node.usage:
            continue
        request_key = node.request_id or node.uuid
        previous = assistant_requests.get(request_key)
        if previous is None or node.ts >= previous.ts:
            assistant_requests[request_key] = node
    return nodes, sorted(assistant_requests.values(), key=lambda item: item.ts)


def claude_cost_entry(node: ClaudeNode) -> CostEntry:
    usage = node.usage or {}
    return CostEntry(
        model=node.model,
        live_input=int(usage.get("input_tokens", 0)),
        cache_write_input=int(usage.get("cache_creation_input_tokens", 0)),
        cache_read_input=int(usage.get("cache_read_input_tokens", 0)),
        output=int(usage.get("output_tokens", 0)),
    )


def resolve_claude_query_root(
    node: ClaudeNode,
    nodes: dict[str, ClaudeNode],
    cache: dict[str, ClaudeNode | None],
) -> ClaudeNode | None:
    current: ClaudeNode | None = node
    visited: list[str] = []
    fallback: ClaudeNode | None = None

    while current is not None and current.uuid not in cache:
        visited.append(current.uuid)
        if current.entry_type == "user":
            fallback = current
            if current.source_tool_assistant_uuid is None and not current.tool_use_result:
                break
        current = nodes.get(current.parent_uuid or "")

    resolved = cache.get(current.uuid) if current is not None and current.uuid in cache else current or fallback
    for visited_uuid in visited:
        cache[visited_uuid] = resolved
    return resolved


def build_claude_query_windows(jsonl_path: pathlib.Path) -> list[QueryWindow]:
    nodes, assistant_nodes = load_claude_nodes(jsonl_path)
    query_root_cache: dict[str, ClaudeNode | None] = {}
    grouped: dict[str, QueryWindow] = {}

    for node in assistant_nodes:
        query_root = resolve_claude_query_root(node, nodes, query_root_cache)
        query_key = query_root.uuid if query_root is not None else node.request_id or node.uuid
        start_ts = query_root.ts if query_root is not None else node.ts
        window = grouped.get(query_key)
        if window is None:
            grouped[query_key] = QueryWindow(
                entries=[claude_cost_entry(node)],
                start_ts=start_ts,
                end_ts=node.ts,
                request_count=1,
            )
            continue
        window.entries.append(claude_cost_entry(node))
        if start_ts < window.start_ts:
            window.start_ts = start_ts
        if node.ts > window.end_ts:
            window.end_ts = node.ts
        window.request_count += 1

    return sorted(grouped.values(), key=lambda item: item.end_ts)


def claude_entries_since(jsonl_path: pathlib.Path, since: datetime) -> tuple[list[CostEntry], datetime | None, int]:
    _, assistant_nodes = load_claude_nodes(jsonl_path)
    filtered_nodes = [node for node in assistant_nodes if node.ts >= since]
    if not filtered_nodes:
        return [], None, 0
    return [claude_cost_entry(node) for node in filtered_nodes], filtered_nodes[-1].ts, len(filtered_nodes)


def latest_claude_entry(jsonl_path: pathlib.Path) -> CostEntry | None:
    _, assistant_nodes = load_claude_nodes(jsonl_path)
    if not assistant_nodes:
        return None
    return claude_cost_entry(assistant_nodes[-1])


def latest_claude_query(jsonl_path: pathlib.Path) -> QueryWindow | None:
    windows = build_claude_query_windows(jsonl_path)
    return windows[-1] if windows else None


def codex_entries_since(source: CodexSource, since: datetime) -> tuple[list[CostEntry], datetime | None, int]:
    entries: list[CostEntry] = []
    previous_sample: CodexSample | None = None
    for sample in source.samples:
        if sample.ts < since:
            previous_sample = sample
            continue

        previous_total_input = previous_sample.total_input if previous_sample else 0
        previous_total_cached = previous_sample.total_cached if previous_sample else 0
        previous_total_output = previous_sample.total_output if previous_sample else 0

        delta_input = sample.total_input - previous_total_input
        delta_cached = sample.total_cached - previous_total_cached
        delta_output = sample.total_output - previous_total_output
        live_input = delta_input - delta_cached

        if delta_input < 0 or delta_cached < 0 or delta_output < 0 or live_input < 0:
            previous_sample = sample
            continue

        entries.append(
            CostEntry(
                model=sample.model,
                live_input=live_input,
                cache_write_input=0,
                cache_read_input=delta_cached,
                output=delta_output,
            )
        )
        previous_sample = sample

    last_ts = source.samples[-1].ts if entries else None
    turn_count = sum(1 for ts in source.turn_timestamps if ts >= since)
    return entries, last_ts, turn_count


def latest_codex_entry(source: CodexSource) -> CostEntry:
    last = source.samples[-1]
    live_input = max(last.last_input - last.last_cached, 0)
    return CostEntry(
        model=last.model,
        live_input=live_input,
        cache_write_input=0,
        cache_read_input=last.last_cached,
        output=last.last_output,
    )


def codex_delta_entry(current: CodexSample, previous: CodexSample | None) -> CostEntry | None:
    previous_total_input = previous.total_input if previous else 0
    previous_total_cached = previous.total_cached if previous else 0
    previous_total_output = previous.total_output if previous else 0

    delta_input = current.total_input - previous_total_input
    delta_cached = current.total_cached - previous_total_cached
    delta_output = current.total_output - previous_total_output
    live_input = delta_input - delta_cached

    if delta_input < 0 or delta_cached < 0 or delta_output < 0 or live_input < 0:
        return None

    return CostEntry(
        model=current.model,
        live_input=live_input,
        cache_write_input=0,
        cache_read_input=delta_cached,
        output=delta_output,
    )


def latest_codex_query(source: CodexSource) -> QueryWindow | None:
    baseline: CodexSample | None = None
    current_query: dict | None = None
    windows: list[QueryWindow] = []

    for event in source.events:
        if event.kind == "task_started":
            if current_query is not None and current_query["last_sample"] is not None:
                entry = codex_delta_entry(current_query["last_sample"], current_query["baseline"])
                if entry is not None:
                    windows.append(
                        QueryWindow(
                            entries=[entry],
                            start_ts=current_query["start_ts"],
                            end_ts=current_query["last_sample"].ts,
                            request_count=current_query["request_count"],
                        )
                    )
                baseline = current_query["last_sample"]
            current_query = {
                "start_ts": event.ts,
                "baseline": baseline,
                "last_sample": None,
                "request_count": 0,
            }
            continue

        if event.kind == "token_count":
            sample = source.samples[event.sample_index] if event.sample_index is not None else None
            if sample is None:
                continue
            if current_query is None:
                baseline = sample
                continue
            current_query["last_sample"] = sample
            current_query["request_count"] += 1
            continue

        if event.kind not in {"task_complete", "turn_aborted"} or current_query is None:
            continue

        last_sample = current_query["last_sample"]
        if last_sample is not None:
            entry = codex_delta_entry(last_sample, current_query["baseline"])
            if entry is not None:
                windows.append(
                    QueryWindow(
                        entries=[entry],
                        start_ts=current_query["start_ts"],
                        end_ts=event.ts,
                        request_count=current_query["request_count"],
                    )
                )
            baseline = last_sample
        current_query = None

    if current_query is not None and current_query["last_sample"] is not None:
        entry = codex_delta_entry(current_query["last_sample"], current_query["baseline"])
        if entry is not None:
            windows.append(
                QueryWindow(
                    entries=[entry],
                    start_ts=current_query["start_ts"],
                    end_ts=current_query["last_sample"].ts,
                    request_count=current_query["request_count"],
                )
            )

    return windows[-1] if windows else None


def compute_cost(entries: list[CostEntry]) -> tuple[int, int, int, int, float, bool]:
    total_live = total_cache_write = total_cache_read = total_output = 0
    total_cost = 0.0
    cost_available = False
    million = 1_000_000

    for entry in entries:
        rates, known = get_pricing(entry.model)
        cost_available = cost_available or known
        total_live += entry.live_input
        total_cache_write += entry.cache_write_input
        total_cache_read += entry.cache_read_input
        total_output += entry.output
        total_cost += (
            (entry.live_input / million) * rates["in"]
            + (entry.cache_write_input / million) * rates["cache_write"]
            + (entry.cache_read_input / million) * rates["cache_read"]
            + (entry.output / million) * rates["out"]
        )

    total_in = total_live + total_cache_write + total_cache_read
    live_and_write = total_live + total_cache_write
    return total_in, total_cache_read, live_and_write, total_output, total_cost, cost_available


def format_budget_result(profile_name: str, live_tokens: int, output_tokens: int) -> str:
    budget = BUDGETS[profile_name]
    over_live = live_tokens > budget["live_max"]
    over_out = output_tokens > budget["out_max"]
    if not over_live and not over_out:
        return (
            f" | budget[{profile_name}]: PASS "
            f"(live {live_tokens:,}/{budget['live_max']:,}, out {output_tokens:,}/{budget['out_max']:,})"
        )

    reasons: list[str] = []
    if over_live:
        reasons.append(f"live {live_tokens:,}>{budget['live_max']:,}")
    if over_out:
        reasons.append(f"out {output_tokens:,}>{budget['out_max']:,}")
    return f" | budget[{profile_name}]: OVER ({'; '.join(reasons)})"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report token counts, estimated cost, and duration for local motion skill runs.")
    parser.add_argument("--since", type=str, default=None, help="ISO timestamp marking the task start.")
    parser.add_argument(
        "--latest-query",
        action="store_true",
        help="Report the most recent finished user query instead of the last request sample.",
    )
    parser.add_argument("--stamp", action="store_true", help="Print the current UTC timestamp.")
    parser.add_argument("--source", choices=["auto", "claude", "codex"], default="auto", help="Metrics source to use.")
    parser.add_argument(
        "--budget",
        choices=sorted(BUDGETS.keys()),
        default=None,
        help="Optional runtime budget profile.",
    )
    parser.add_argument("--list-budgets", action="store_true", help="List available runtime budget profiles and exit.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.stamp:
        print(datetime.now(timezone.utc).isoformat())
        return

    if args.list_budgets:
        for profile_name, budget in BUDGETS.items():
            print(
                f"{profile_name}: {budget['label']} "
                f"(live<={budget['live_max']:,}, out<={budget['out_max']:,})"
            )
        return

    since_dt = None
    if args.since is not None:
        try:
            since_dt = parse_timestamp(args.since)
        except (TypeError, ValueError):
            print(f"metrics: invalid timestamp '{args.since}'")
            return
    if since_dt is not None and args.latest_query:
        print("metrics: use either --since or --latest-query, not both")
        return

    source_name, source = choose_source(os.getcwd(), args.source)
    if source is None or source_name is None:
        print("metrics: no matching local Claude or Codex session found — cost unavailable")
        return

    duration_label = ""
    turns_label = ""

    if source_name == "claude":
        claude_source: ClaudeSource = source  # type: ignore[assignment]
        if args.latest_query:
            query_window = latest_claude_query(claude_source.jsonl_path)
            if query_window is None:
                print("metrics: no completed Claude query found — cost unavailable")
                return
            priced_entries = query_window.entries
            duration_label = f"duration: {format_duration((query_window.end_ts - query_window.start_ts).total_seconds())} | "
            turns_label = f"  [{query_window.request_count} request{'s' if query_window.request_count != 1 else ''}]"
        elif since_dt is None:
            latest = latest_claude_entry(claude_source.jsonl_path)
            if latest is None:
                print("metrics: no assistant entry found — cost unavailable")
                return
            priced_entries = [latest]
        else:
            priced_entries, last_ts, request_count = claude_entries_since(claude_source.jsonl_path, since_dt)
            if not priced_entries:
                print("metrics: no assistant entries found after start timestamp — JSONL may not have flushed yet")
                return
            if last_ts is not None:
                duration_label = f"duration: {format_duration((last_ts - since_dt).total_seconds())} | "
            turns_label = f"  [{request_count} request{'s' if request_count != 1 else ''}]"
    else:
        codex_source: CodexSource = source  # type: ignore[assignment]
        if args.latest_query:
            query_window = latest_codex_query(codex_source)
            if query_window is None:
                print("metrics: no completed Codex query found — cost unavailable")
                return
            priced_entries = query_window.entries
            duration_label = f"duration: {format_duration((query_window.end_ts - query_window.start_ts).total_seconds())} | "
            turns_label = f"  [{query_window.request_count} request{'s' if query_window.request_count != 1 else ''}]"
        elif since_dt is None:
            priced_entries = [latest_codex_entry(codex_source)]
        else:
            priced_entries, last_ts, turn_count = codex_entries_since(codex_source, since_dt)
            if not priced_entries or last_ts is None:
                print("metrics: no Codex token updates found after start timestamp — session may not have flushed yet")
                return
            duration_label = f"duration: {format_duration((last_ts - since_dt).total_seconds())} | "
            turns_label = f"  [{turn_count} turn{'s' if turn_count != 1 else ''}]"

    total_in, cached, live_write, output, cost, cost_available = compute_cost(priced_entries)
    cost_label = f"~${cost:.4f}" if cost_available else "unavailable"
    budget_label = format_budget_result(args.budget, live_write, output) if args.budget else ""

    print(
        f"{duration_label}"
        f"tokens: {total_in:,} in "
        f"({cached:,} cached + {live_write:,} live) "
        f"/ {output:,} out | estimated cost: {cost_label}"
        f"{budget_label}"
        f"{turns_label}"
    )


if __name__ == "__main__":
    main()
