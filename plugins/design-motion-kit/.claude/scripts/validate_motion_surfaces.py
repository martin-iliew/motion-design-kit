from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT.parent / ".claude-plugin" / "plugin.json"
REGISTRY_PATH = ROOT / "motion-registry.yaml"

MOTION_COMMANDS = {
    "motion-build",
    "motion-upgrade",
    "motion-audit",
    "motion-discover",
    "motion-refresh",
}
REQUIRED_SHARED = {
    ".claude/shared/execution-modes.md",
    ".claude/shared/bundle-loading.md",
    ".claude/shared/motion-runtime-selection.md",
    ".claude/shared/motion-guardrails.md",
    ".claude/shared/motion-audit-rules.md",
    ".claude/shared/handoff-contracts.md",
    ".claude/shared/validation.md",
    ".claude/shared/output-contracts.md",
}


def main() -> None:
    plugin = json.loads(PLUGIN_PATH.read_text(encoding="utf-8"))
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))

    plugin_commands = {Path(item).stem for item in plugin["commands"]}
    plugin_skills = {Path(item).name for item in plugin["skills"]}
    registry_commands = set(registry["commands"]["canonical"].keys())
    registry_skills = set(registry["skills"]["canonical"])

    if registry_commands != MOTION_COMMANDS or registry_skills != MOTION_COMMANDS:
        raise SystemExit("motion-registry.yaml does not define the expected canonical motion surface")
    if not MOTION_COMMANDS.issubset(plugin_commands):
        raise SystemExit("plugin.json does not include the full motion command surface")
    if not MOTION_COMMANDS.issubset(plugin_skills):
        raise SystemExit("plugin.json does not include the full motion skill surface")

    for name in MOTION_COMMANDS:
        if not (ROOT / "commands" / f"{name}.md").exists():
            raise SystemExit(f"missing command file: {name}")
        skill_path = ROOT / "skills" / name / "SKILL.md"
        if not skill_path.exists():
            raise SystemExit(f"missing skill file: {name}")
        text = skill_path.read_text(encoding="utf-8")
        if name in {"motion-build", "motion-upgrade", "motion-audit"} and ".claude/shared/" not in text:
            raise SystemExit(f"{name} must load the merged shared layer")

    for relative in REQUIRED_SHARED:
        if not (ROOT.parent / relative).exists():
            raise SystemExit(f"missing shared file: {relative}")

    print("motion surfaces valid")


if __name__ == "__main__":
    main()
