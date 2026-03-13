from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import yaml

from compile_design_library import main as compile_library


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "design-library" / "catalog.yaml"


def infer_status(score: int) -> str:
    if score >= 9:
        return "core"
    if score >= 8:
        return "evergreen"
    return "watch"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--last-reviewed", default=date.today().strftime("%Y-%m"))
    args = parser.parse_args()

    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        catalog = yaml.safe_load(handle)

    for pattern in catalog["patterns"]:
        if pattern.get("manual_override"):
            continue
        pattern["last_reviewed"] = args.last_reviewed
        pattern["status"] = infer_status(int(pattern["trend_score"]))

    with CATALOG_PATH.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(catalog, handle, sort_keys=False, allow_unicode=False)

    compile_library()


if __name__ == "__main__":
    main()
