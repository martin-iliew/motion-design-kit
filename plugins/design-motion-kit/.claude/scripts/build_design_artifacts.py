from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from dtcg_to_tailwind_theme import build_theme_bundle, load_json, write_json, write_theme_css


ROOT = Path(__file__).resolve().parents[1]
DESIGN_LIB = ROOT / "design-library"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_yaml(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)


def validate_brief_dir(brief_dir: Path) -> dict[str, Path]:
    required = {
        "brief": brief_dir / "brief.json",
        "copy": brief_dir / "copy.md",
        "images": brief_dir / "images.json",
        "tokens": brief_dir / "tokens.dtcg.json",
    }
    missing = [str(path) for path in required.values() if not path.exists()]
    if missing:
        raise SystemExit(f"missing brief inputs: {missing}")
    return required


def resolve_context(brief: dict, baselines: dict) -> str:
    for key in ("page_type", "site_context", "context"):
        value = brief.get(key)
        if value in baselines:
            return value
    return "any"


def required_surfaces(brief: dict, baselines: dict, context: str) -> list[str]:
    explicit = brief.get("required_surfaces")
    if isinstance(explicit, list) and explicit:
        return [str(item) for item in explicit]
    return list(baselines.get(context, {}).get("required_sections", ["hero", "proof", "cta"]))


def select_patterns(scores: dict, context: str, surfaces: list[str]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for surface in surfaces:
        contexts = scores.get(surface, {})
        ranked = contexts.get(context) or contexts.get("any") or []
        if not ranked:
            continue
        selected.append({"surface": surface, "pattern_id": ranked[0]})
    return selected


def load_pattern(pattern_id: str, catalog_by_id: dict) -> dict:
    entry = catalog_by_id[pattern_id]
    folder = DESIGN_LIB / entry["folder"]
    return {
        "catalog": entry,
        "spec": load_yaml(folder / "spec.yaml"),
        "composition": load_yaml(folder / entry["composition"]),
    }


def unique_component_inventory(patterns: list[dict]) -> list[str]:
    inventory: list[str] = []
    seen = set()
    for pattern in patterns:
        for item in pattern["composition"].get("component_inventory", []):
            if item not in seen:
                inventory.append(item)
                seen.add(item)
    return inventory


def build_motion_hints(context: str, patterns: list[dict]) -> dict:
    hints = []
    for pattern in patterns:
        for target in pattern["composition"].get("motion_ready", {}).get("targets", []):
            hints.append(
                {
                    "surface": pattern["catalog"]["category"],
                    "pattern_id": pattern["catalog"]["id"],
                    "target_id": target["id"],
                    "role": target["role"],
                    "allowed_families": target.get("allowed_families", []),
                    "intensity": target.get("intensity", "low"),
                }
            )
    return {
        "version": "1",
        "page_context": context,
        "hints": hints,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    brief_dir = Path(args.brief_dir)
    out_dir = Path(args.out_dir)
    paths = validate_brief_dir(brief_dir)

    brief = load_json(paths["brief"])
    _ = load_json(paths["images"])
    _ = paths["copy"].read_text(encoding="utf-8")
    token_payload = load_json(paths["tokens"])

    scores = load_yaml(DESIGN_LIB / "scores.yaml")
    baselines = load_yaml(DESIGN_LIB / "site-baselines.yaml")
    catalog = load_yaml(DESIGN_LIB / "catalog.yaml")["patterns"]
    catalog_by_id = {entry["id"]: entry for entry in catalog}

    context = resolve_context(brief, baselines)
    surfaces = required_surfaces(brief, baselines, context)
    selected = select_patterns(scores, context, surfaces)
    loaded_patterns = [load_pattern(entry["pattern_id"], catalog_by_id) for entry in selected]

    variables, aliases = build_theme_bundle(token_payload)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_theme_css(out_dir / "theme.css", variables)
    write_json(out_dir / "token-aliases.json", aliases)

    decision_pack = {
        "version": "1",
        "page_context": context,
        "brief": {
            "audience": brief.get("audience"),
            "goal": brief.get("goal"),
            "constraints": brief.get("constraints", []),
        },
        "selected_patterns": [
            {
                "surface": item["surface"],
                "pattern_id": pattern["catalog"]["id"],
                "folder": pattern["catalog"]["folder"],
                "composition_file": pattern["catalog"]["composition"],
            }
            for item, pattern in zip(selected, loaded_patterns)
        ],
        "component_inventory": unique_component_inventory(loaded_patterns),
        "implementation_notes": {
            "theme_css": "brief/theme.css",
            "token_aliases": "brief/token-aliases.json",
            "no_raw_values": True,
        },
    }
    write_yaml(out_dir / "design-decision-pack.yaml", decision_pack)
    write_yaml(out_dir / "motion-hints.yaml", build_motion_hints(context, loaded_patterns))

    print(
        json.dumps(
            {
                "context": context,
                "surfaces": surfaces,
                "patterns": [item["pattern_id"] for item in selected],
                "theme_variables": len(variables),
            }
        )
    )


if __name__ == "__main__":
    main()
