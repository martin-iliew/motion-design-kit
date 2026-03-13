from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT.parent / ".claude-plugin" / "plugin.json"
REGISTRY_PATH = ROOT / "web-registry.yaml"


def main() -> None:
    with PLUGIN_PATH.open("r", encoding="utf-8") as handle:
        plugin = json.load(handle)
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        registry = yaml.safe_load(handle)

    command_files = plugin["commands"]
    skill_dirs = plugin["skills"]
    if len(command_files) != 5 or len(skill_dirs) != 5:
        raise SystemExit("plugin surface must expose exactly five commands and five skills")

    canonical_commands = set(registry["commands"]["canonical"].keys())
    canonical_skills = set(registry["skills"]["canonical"])
    plugin_commands = {Path(item).stem for item in command_files}
    plugin_skills = {Path(item).name for item in skill_dirs}
    listed_commands = set(registry["plugin"]["commands"])
    listed_skills = set(registry["plugin"]["skills"])

    if canonical_commands != plugin_commands or canonical_commands != listed_commands:
        raise SystemExit("command registry mismatch")
    if canonical_skills != plugin_skills or canonical_skills != listed_skills:
        raise SystemExit("skill registry mismatch")

    for relative in command_files:
        if not (ROOT.parent / relative).exists():
            raise SystemExit(f"missing command file: {relative}")
    for relative in skill_dirs:
        if not (ROOT.parent / relative / "SKILL.md").exists():
            raise SystemExit(f"missing skill file: {relative}/SKILL.md")

    print("design surfaces valid")


if __name__ == "__main__":
    main()
