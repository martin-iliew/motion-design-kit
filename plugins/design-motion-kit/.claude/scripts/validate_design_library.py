from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT / "design-library"
CATALOG_PATH = LIB_DIR / "catalog.yaml"
REQUIRED_ENTRY_FIELDS = {
    "id",
    "name",
    "category",
    "framework",
    "surfaces",
    "site_contexts",
    "folder",
    "composition",
    "description",
    "trend_score",
    "status",
    "conversion_signal",
    "last_reviewed",
    "sources",
    "manual_override",
    "notes",
}
ALLOWED_STATUSES = {"core", "evergreen", "watch"}
HTML_MARKERS = ("<section", "<div", "<article", "<header", "</", "<h1", "<h2", "<p>")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-count", type=int)
    args = parser.parse_args()

    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        catalog = yaml.safe_load(handle)

    patterns = catalog.get("patterns", [])
    ids = set()
    for pattern in patterns:
        missing = REQUIRED_ENTRY_FIELDS - set(pattern)
        if missing:
            raise SystemExit(f"missing catalog fields for {pattern.get('id', '<unknown>')}: {sorted(missing)}")
        if pattern["id"] in ids:
            raise SystemExit(f"duplicate pattern id: {pattern['id']}")
        if int(pattern["trend_score"]) < 1 or int(pattern["trend_score"]) > 10:
            raise SystemExit(f"trend_score out of range for {pattern['id']}")
        if pattern["status"] not in ALLOWED_STATUSES:
            raise SystemExit(f"invalid status for {pattern['id']}: {pattern['status']}")

        folder = LIB_DIR / pattern["folder"]
        composition = folder / pattern["composition"]
        for path in (folder / "index.md", folder / "spec.yaml", composition):
            if not path.exists():
                raise SystemExit(f"missing required file for {pattern['id']}: {path}")

        composition_text = composition.read_text(encoding="utf-8")
        if any(marker in composition_text.lower() for marker in HTML_MARKERS):
            raise SystemExit(f"composition.yaml must be non-code for {pattern['id']}")
        yaml.safe_load(composition_text)
        ids.add(pattern["id"])

    if args.expected_count is not None and len(patterns) != args.expected_count:
        raise SystemExit(f"expected {args.expected_count} patterns, found {len(patterns)}")

    print(f"design library valid: {len(patterns)} patterns")


if __name__ == "__main__":
    main()
