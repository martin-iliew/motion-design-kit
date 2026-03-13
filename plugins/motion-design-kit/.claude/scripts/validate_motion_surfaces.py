#!/usr/bin/env python3
"""
Validate canonical motion command and skill surfaces inside the shipped plugin payload.

Checks:
- registry structure, canonical names, and execution modes
- command -> skill routing and mode syntax
- plugin exports
- query_cost budget names
- removal of old canonical entrypoints
- canonical build/upgrade skills load shared references instead of inlining old workflow blocks
- no stray deprecated canonical references inside .claude
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import yaml


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
CLAUDE_DIR = REPO_ROOT / ".claude"
PLUGIN_PATH = REPO_ROOT / ".claude-plugin" / "plugin.json"
REGISTRY_PATH = CLAUDE_DIR / "motion-registry.yaml"
COMMANDS_DIR = CLAUDE_DIR / "commands"
SKILLS_DIR = CLAUDE_DIR / "skills"
QUERY_COST_PATH = CLAUDE_DIR / "scripts" / "query_cost.py"
VALIDATOR_PATH = CLAUDE_DIR / "scripts" / "validate_motion_surfaces.py"

DEPRECATED_SKILL_PATHS = [
    SKILLS_DIR / "motion-dev" / "SKILL.md",
    SKILLS_DIR / "motion-enhance" / "SKILL.md",
]
DEPRECATED_COMMAND_PATHS = [
    COMMANDS_DIR / "motion-dev.md",
    COMMANDS_DIR / "motion-enhance.md",
]
ALLOWED_DEPRECATED_NAME_PATHS = {VALIDATOR_PATH}
DEPRECATED_NAMES = {"motion-dev", "motion-enhance"}
COMMAND_SKILL_RE = re.compile(r"invoke the `([^`]+)` skill", re.IGNORECASE)

REQUIRED_SHARED_REFERENCES = [
    SKILLS_DIR / "shared" / "runtime-selection.md",
    SKILLS_DIR / "shared" / "execution-modes.md",
    SKILLS_DIR / "shared" / "guardrails.md",
    SKILLS_DIR / "shared" / "output-contracts.md",
]

REQUIRED_MODE_NAMES = {"fast", "balanced", "premium"}

REQUIRED_COMMAND_TOOLS = {
    "motion-build": {"Read", "Edit", "Bash"},
    "motion-upgrade": {"Read", "Edit", "Bash"},
    "motion-audit": {"Read", "Bash"},
    "motion-discover": {"Read", "Write", "Edit", "WebSearch", "WebFetch", "Agent", "Bash"},
    "motion-refresh": {"Read", "Edit", "WebSearch", "WebFetch", "Bash"},
}

FORBIDDEN_COMMAND_TOOLS = {
    "motion-audit": {"Edit"},
}

SKILL_SHARED_EXPECTATIONS = {
    "motion-build": [
        ".claude/skills/shared/runtime-selection.md",
        ".claude/skills/shared/execution-modes.md",
        ".claude/skills/shared/guardrails.md",
        ".claude/skills/shared/output-contracts.md",
    ],
    "motion-upgrade": [
        ".claude/skills/shared/runtime-selection.md",
        ".claude/skills/shared/execution-modes.md",
        ".claude/skills/shared/guardrails.md",
        ".claude/skills/shared/output-contracts.md",
    ],
    "motion-audit": [
        ".claude/skills/shared/audit-rules.md",
        ".claude/skills/shared/output-contracts.md",
    ],
}

SKILL_WORKFLOW_EXPECTATIONS = {
    "motion-build": ["/motion-discover"],
    "motion-discover": [
        ".claude/skills/motion-discover/references/catalog-contract.md",
        "python .claude/scripts/validate_motion_library.py --expected-count <current-catalog-size>",
    ],
    "motion-refresh": [
        ".claude/skills/motion-refresh/references/runtime-outputs.md",
        "python .claude/scripts/validate_motion_library.py --expected-count <current-catalog-size>",
    ],
}

FORBIDDEN_INLINE_MARKERS = {
    "motion-build": [
        "Inline Pattern Map",
        "Motion Personality",
        "Stack Detection",
        "Session Metrics",
        "query_cost.py --latest-query",
    ],
    "motion-upgrade": [
        "Then ask:",
        "Token Budget Guide",
        "### Metrics",
        "query_cost.py --latest-query",
    ],
    "motion-audit": [
        "### Metrics",
        "query_cost.py --latest-query",
        "Pre-flight — Query-scoped metrics",
        "Want me to apply all CRITICAL fixes directly",
        "Apply each CRITICAL fix to the file",
    ],
}

REFERENCE_EXPECTATIONS = {
    SKILLS_DIR / "motion-build" / "references" / "stack-patterns.md": {
        "required": ["https://cdn.jsdelivr.net/npm/gsap@3.14/dist/gsap.min.js"],
        "forbidden": ["https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"],
    },
    SKILLS_DIR / "motion-build" / "references" / "motion-spec-translation-guide.md": {
        "required": ["autoAlpha"],
        "forbidden": ['gsap.set("[target.selector]", { opacity: 1, clearProps: "y" })'],
    },
    SKILLS_DIR / "motion-discover" / "references" / "gsap-cheatsheet.md": {
        "required": ["autoAlpha"],
        "forbidden": ['gsap.from(".el", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out" });'],
    },
}


def load_registry() -> dict:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


def load_plugin_manifest() -> dict:
    return json.loads(PLUGIN_PATH.read_text(encoding="utf-8"))


def load_query_cost_module():
    spec = importlib.util.spec_from_file_location("query_cost_module", QUERY_COST_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load query_cost.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def command_target(command_name: str) -> str | None:
    path = COMMANDS_DIR / f"{command_name}.md"
    match = COMMAND_SKILL_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def load_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def parse_allowed_tools(value: object) -> set[str]:
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    if isinstance(value, str):
        return {item.strip() for item in value.split(",") if item.strip()}
    return set()


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def validate_execution_modes(registry: dict, errors: list[str]) -> None:
    execution_modes = registry.get("execution_modes")
    if not isinstance(execution_modes, dict):
        errors.append("motion-registry.yaml is missing execution_modes")
        return

    if execution_modes.get("default") != "balanced":
        errors.append("execution_modes.default must be 'balanced'")

    supported = execution_modes.get("supported")
    if not isinstance(supported, dict):
        errors.append("execution_modes.supported must be a mapping")
        return

    supported_names = set(supported.keys())
    if supported_names != REQUIRED_MODE_NAMES:
        errors.append(
            f"execution_modes.supported must be exactly {sorted(REQUIRED_MODE_NAMES)}; found {sorted(supported_names)}"
        )


def validate_command_docs(command_name: str, errors: list[str]) -> None:
    command_path = COMMANDS_DIR / f"{command_name}.md"
    text = command_path.read_text(encoding="utf-8")
    if "mode: fast|balanced|premium" not in text:
        errors.append(f"{rel(command_path)} must document mode: fast|balanced|premium")
    if "balanced" not in text:
        errors.append(f"{rel(command_path)} must mention the balanced default mode")


def validate_command_tools(command_name: str, errors: list[str]) -> None:
    command_path = COMMANDS_DIR / f"{command_name}.md"
    front_matter = load_front_matter(command_path)
    allowed_tools = parse_allowed_tools(front_matter.get("allowed-tools"))

    for required_tool in REQUIRED_COMMAND_TOOLS.get(command_name, set()):
        if required_tool not in allowed_tools:
            errors.append(f"{rel(command_path)} must allow tool {required_tool}")

    for forbidden_tool in FORBIDDEN_COMMAND_TOOLS.get(command_name, set()):
        if forbidden_tool in allowed_tools:
            errors.append(f"{rel(command_path)} must not allow tool {forbidden_tool}")

    if command_name == "motion-discover" and not front_matter.get("argument-hint"):
        errors.append(f"{rel(command_path)} must include an argument-hint")


def validate_canonical_skill(skill_name: str, errors: list[str]) -> None:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")

    for required_text in SKILL_SHARED_EXPECTATIONS.get(skill_name, []):
        if required_text not in text:
            errors.append(f"{rel(skill_path)} must load shared reference {required_text}")

    for required_text in SKILL_WORKFLOW_EXPECTATIONS.get(skill_name, []):
        if required_text not in text:
            errors.append(f"{rel(skill_path)} must document workflow requirement {required_text}")

    for forbidden_text in FORBIDDEN_INLINE_MARKERS.get(skill_name, []):
        if forbidden_text in text:
            errors.append(
                f"{rel(skill_path)} still contains inline legacy workflow marker '{forbidden_text}'"
            )


def validate_reference_examples(errors: list[str]) -> None:
    for path, expectations in REFERENCE_EXPECTATIONS.items():
        text = path.read_text(encoding="utf-8")
        for required_text in expectations.get("required", []):
            if required_text not in text:
                errors.append(f"{rel(path)} must contain reference marker '{required_text}'")
        for forbidden_text in expectations.get("forbidden", []):
            if forbidden_text in text:
                errors.append(f"{rel(path)} still contains stale reference marker '{forbidden_text}'")


def validate_audit_surface(errors: list[str]) -> None:
    output_contracts_path = SKILLS_DIR / "shared" / "output-contracts.md"
    text = output_contracts_path.read_text(encoding="utf-8")
    stale_prompt = "may end with a short follow-up question offering to apply the critical fixes"
    if stale_prompt in text:
        errors.append(f"{rel(output_contracts_path)} still treats motion-audit as a mutating follow-up flow")


def main() -> int:
    errors: list[str] = []

    registry = load_registry()
    plugin = load_plugin_manifest()
    query_cost = load_query_cost_module()

    canonical_skills = registry["skills"]["canonical"]
    canonical_commands = registry["commands"]["canonical"]
    plugin_commands = registry["plugin"]["commands"]
    plugin_skills = registry["plugin"]["skills"]
    canonical_budgets = registry["budgets"]["canonical"]

    validate_execution_modes(registry, errors)

    for shared_path in REQUIRED_SHARED_REFERENCES:
        if not shared_path.exists():
            errors.append(f"Missing shared reference: {rel(shared_path)}")

    for skill_name in canonical_skills:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"Missing canonical skill file: {rel(skill_path)}")

    for old_path in DEPRECATED_SKILL_PATHS:
        if old_path.exists():
            errors.append(f"Deprecated skill entrypoint still exists: {rel(old_path)}")
    for old_path in DEPRECATED_COMMAND_PATHS:
        if old_path.exists():
            errors.append(f"Deprecated command file still exists: {rel(old_path)}")

    for command_name, skill_name in canonical_commands.items():
        command_path = COMMANDS_DIR / f"{command_name}.md"
        if not command_path.exists():
            errors.append(f"Missing command file: {rel(command_path)}")
            continue
        target = command_target(command_name)
        if target != skill_name:
            errors.append(
                f"Command {command_name} routes to {target or 'nothing'}; expected {skill_name}"
            )
        if command_name in {"motion-build", "motion-upgrade"}:
            validate_command_docs(command_name, errors)
        validate_command_tools(command_name, errors)

    expected_plugin_command_paths = [f"./.claude/commands/{name}.md" for name in plugin_commands]
    expected_plugin_skill_paths = [f"./.claude/skills/{name}" for name in plugin_skills]
    if plugin.get("commands") != expected_plugin_command_paths:
        errors.append("plugin.json commands do not match registry plugin.commands order")
    if plugin.get("skills") != expected_plugin_skill_paths:
        errors.append("plugin.json skills do not match registry plugin.skills order")

    actual_budgets = getattr(query_cost, "BUDGETS", {})
    if actual_budgets != canonical_budgets:
        errors.append("query_cost.py BUDGETS do not match registry canonical budgets")

    for skill_name in {"motion-build", "motion-upgrade", "motion-audit", "motion-discover", "motion-refresh"}:
        validate_canonical_skill(skill_name, errors)

    validate_reference_examples(errors)
    validate_audit_surface(errors)

    for path in CLAUDE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path in ALLOWED_DEPRECATED_NAME_PATHS:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for deprecated_name in DEPRECATED_NAMES:
            if deprecated_name in text:
                errors.append(
                    f"Deprecated canonical name '{deprecated_name}' still present in {rel(path)}"
                )

    if errors:
        print("Motion surface validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Motion surface validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
