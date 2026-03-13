from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "design-motion-kit"
FIXTURE_ROOT = REPO_ROOT / "evals" / "fixtures" / "design-motion-kit"


def main() -> None:
    fixture_brief = FIXTURE_ROOT / "brief"
    if not fixture_brief.exists():
        raise SystemExit(f"missing fixture brief: {fixture_brief}")

    tmp_root = REPO_ROOT / "_tmp_design_motion_pipeline"
    if tmp_root.exists():
        shutil.rmtree(tmp_root, ignore_errors=True)
    tmp_root.mkdir(parents=True, exist_ok=True)
    try:
        tmp_brief = tmp_root / "brief"
        shutil.copytree(fixture_brief, tmp_brief)
        command = [
            "python",
            str(PLUGIN_ROOT / ".claude" / "scripts" / "build_design_artifacts.py"),
            "--brief-dir",
            str(tmp_brief),
            "--out-dir",
            str(tmp_brief),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(result.stderr or result.stdout)

        theme_css = (tmp_brief / "theme.css").read_text(encoding="utf-8")
        aliases = json.loads((tmp_brief / "token-aliases.json").read_text(encoding="utf-8"))
        decision_pack = yaml.safe_load((tmp_brief / "design-decision-pack.yaml").read_text(encoding="utf-8"))
        motion_hints = yaml.safe_load((tmp_brief / "motion-hints.yaml").read_text(encoding="utf-8"))

        if "@theme" not in theme_css:
            raise SystemExit("theme.css did not contain @theme")
        if not aliases:
            raise SystemExit("token-aliases.json is empty")
        if not decision_pack["selected_patterns"]:
            raise SystemExit("design decision pack has no selected patterns")

        selected_pattern_ids = {item["pattern_id"] for item in decision_pack["selected_patterns"]}
        hinted_pattern_ids = {item["pattern_id"] for item in motion_hints["hints"]}
        if not hinted_pattern_ids.issubset(selected_pattern_ids):
            raise SystemExit("motion hints reference patterns not present in the decision pack")

        print("design pipeline valid")
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    main()
