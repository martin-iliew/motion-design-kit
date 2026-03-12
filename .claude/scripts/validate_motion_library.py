from __future__ import annotations

import argparse
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
LIB_DIR = ROOT / ".claude" / "motion-library"
CATALOG_PATH = LIB_DIR / "catalog.yaml"
SCORES_PATH = LIB_DIR / "scores.yaml"
OVERVIEW_PATH = LIB_DIR / "trends-overview.md"
GENERATOR_PATH = ROOT / ".claude" / "scripts" / "generate_motion_library.py"

REQUIRED_SCORE_BUCKETS = [
    "menu",
    "tabs",
    "accordion",
    "modal",
    "drawer",
    "toast",
    "tooltip",
    "form",
    "input",
    "gallery",
    "carousel",
    "media",
    "image",
    "video",
    "svg",
    "icon",
    "loader",
    "timeline",
    "progress-bar",
    "hotspot",
]


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(expected_count: int | None) -> dict:
    issues: list[str] = []

    catalog = load_yaml(CATALOG_PATH)["patterns"]
    scores = load_yaml(SCORES_PATH)
    overview = OVERVIEW_PATH.read_text(encoding="utf-8")

    ids = [entry["id"] for entry in catalog]
    id_set = set(ids)
    folders = sorted(path for path in LIB_DIR.iterdir() if path.is_dir())

    if expected_count is not None and len(catalog) != expected_count:
        issues.append(f"catalog count {len(catalog)} != expected {expected_count}")
    if len(catalog) != len(id_set):
        issues.append("catalog contains duplicate pattern ids")
    if len(folders) != len(catalog):
        issues.append(f"folder count {len(folders)} != catalog count {len(catalog)}")

    for entry in catalog:
        folder = LIB_DIR / entry["folder"]
        snippet_path = folder / entry["snippet"]
        expected_files = sorted(["index.md", "spec.yaml", entry["snippet"]])
        actual_files = sorted(child.name for child in folder.iterdir() if child.is_file()) if folder.exists() else []

        if not folder.is_dir():
            issues.append(f"missing folder for {entry['id']}: {folder}")
            continue
        if not snippet_path.exists():
            issues.append(f"missing snippet for {entry['id']}: {snippet_path.name}")
        if actual_files != expected_files:
            issues.append(f"{entry['id']} file contract mismatch: {actual_files} != {expected_files}")

        if snippet_path.exists():
            text = snippet_path.read_text(encoding="utf-8")
            lowered = text.lower()
            if "import " in lowered or "<script" in lowered or "cdn.jsdelivr" in lowered or "unpkg.com" in lowered:
                issues.append(f"{entry['id']} snippet contains setup/import/CDN leakage")
            if snippet_path.suffix == ".js" and "gsap.matchMedia()" not in text:
                issues.append(f"{entry['id']} snippet.js is missing gsap.matchMedia()")

    overview_count = sum(1 for line in overview.splitlines() if line.startswith("### "))
    if overview_count != len(catalog):
        issues.append(f"trends-overview count {overview_count} != catalog count {len(catalog)}")

    score_ids = set()
    for bucket, contexts in scores.items():
        if bucket == "site_contexts":
            continue
        if not isinstance(contexts, dict):
            issues.append(f"scores bucket {bucket} is not a mapping")
            continue
        for context_name, pattern_ids in contexts.items():
            if not isinstance(pattern_ids, list):
                issues.append(f"scores bucket {bucket}.{context_name} is not a list")
                continue
            for pattern_id in pattern_ids:
                score_ids.add(pattern_id)
                if pattern_id not in id_set:
                    issues.append(f"scores bucket {bucket}.{context_name} references unknown id {pattern_id}")

    for bucket in REQUIRED_SCORE_BUCKETS:
        if bucket not in scores:
            issues.append(f"scores is missing required bucket {bucket}")

    catalog_by_id = {entry["id"]: entry for entry in catalog}
    for pattern_id in score_ids:
        if catalog_by_id[pattern_id]["status"] == "declining":
            issues.append(f"declining pattern {pattern_id} appears in scores.yaml")

    if GENERATOR_PATH.exists():
        generator = SourceFileLoader("motion_library_generator", str(GENERATOR_PATH)).load_module()
        generated = generator.derive_new_patterns()
        generated_ids = [entry["id"] for entry in generated]
        if len(generated_ids) != len(set(generated_ids)):
            issues.append("generator derive_new_patterns() returned duplicate ids")
        missing_generated = [pattern_id for pattern_id in generated_ids if pattern_id not in id_set]
        if missing_generated:
            issues.append(f"catalog is missing generator-defined ids: {missing_generated[:5]}")

    return {
        "ok": not issues,
        "catalog_count": len(catalog),
        "unique_ids": len(id_set),
        "folder_count": len(folders),
        "overview_count": overview_count,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the motion-library corpus and lookup indexes.")
    parser.add_argument("--expected-count", type=int, default=None, help="Optional expected catalog/folder count.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    args = parser.parse_args()

    result = validate(args.expected_count)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"catalog_count: {result['catalog_count']}")
        print(f"unique_ids: {result['unique_ids']}")
        print(f"folder_count: {result['folder_count']}")
        print(f"overview_count: {result['overview_count']}")
        if result["issues"]:
            print("issues:")
            for issue in result["issues"]:
                print(f"- {issue}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
