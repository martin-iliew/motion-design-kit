from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT.parent / ".claude-plugin" / "plugin.json"
REGISTRY_PATH = ROOT / "design-registry.yaml"

DESIGN_COMMANDS = {
    "design-build",
    "design-upgrade",
    "design-audit",
    "design-discover",
    "design-refresh",
}
REQUIRED_SHARED = {
    ".claude/shared/execution-modes.md",
    ".claude/shared/bundle-loading.md",
    ".claude/shared/design-runtime-selection.md",
    ".claude/shared/design-guardrails.md",
    ".claude/shared/design-audit-rules.md",
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

    if registry_commands != DESIGN_COMMANDS or registry_skills != DESIGN_COMMANDS:
        raise SystemExit("design-registry.yaml does not define the expected canonical design surface")
    if not DESIGN_COMMANDS.issubset(plugin_commands):
        raise SystemExit("plugin.json does not include the full design command surface")
    if not DESIGN_COMMANDS.issubset(plugin_skills):
        raise SystemExit("plugin.json does not include the full design skill surface")

    for name in DESIGN_COMMANDS:
        if not (ROOT / "commands" / f"{name}.md").exists():
            raise SystemExit(f"missing command file: {name}")
        skill_path = ROOT / "skills" / name / "SKILL.md"
        if not skill_path.exists():
            raise SystemExit(f"missing skill file: {name}")
        text = skill_path.read_text(encoding="utf-8")
        if ".claude/shared/" not in text:
            raise SystemExit(f"{name} must load the merged shared layer")

    for relative in REQUIRED_SHARED:
        if not (ROOT.parent / relative).exists():
            raise SystemExit(f"missing shared file: {relative}")

    for internal in ("design-system", "design-coder", "vite-react-bootstrap"):
        if not (ROOT / "skills" / "internal" / internal / "SKILL.md").exists():
            raise SystemExit(f"missing internal skill: {internal}")

    print("design surfaces valid")


if __name__ == "__main__":
    main()
