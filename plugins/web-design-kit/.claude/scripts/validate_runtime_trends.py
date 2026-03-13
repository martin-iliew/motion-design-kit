from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT / "design-library"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> None:
    catalog = load_yaml(LIB_DIR / "catalog.yaml")
    scores = load_yaml(LIB_DIR / "scores.yaml")
    baselines = load_yaml(LIB_DIR / "site-baselines.yaml")
    watchlist = load_yaml(LIB_DIR / "trend-watchlist.yaml")

    ids = {pattern["id"] for pattern in catalog["patterns"]}

    for surface, contexts in scores.items():
        if not isinstance(contexts, dict):
            raise SystemExit(f"surface '{surface}' must map to contexts")
        for context, pattern_ids in contexts.items():
            for pattern_id in pattern_ids:
                if pattern_id not in ids:
                    raise SystemExit(f"unknown pattern id in scores.yaml: {surface}.{context}.{pattern_id}")

    for context in ("saas", "ai", "enterprise", "developer-tools", "ecommerce", "any"):
        if context not in baselines:
            raise SystemExit(f"missing site baseline for {context}")

    for group in ("rising", "stable", "watch"):
        for item in watchlist[group]:
            pattern_id = item["id"]
            if pattern_id not in ids:
                raise SystemExit(f"unknown pattern id in trend-watchlist.yaml: {pattern_id}")

    print("runtime trends valid")


if __name__ == "__main__":
    main()
