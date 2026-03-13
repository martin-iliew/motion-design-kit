from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from runtime_trend_compiler import load_runtime_trend_files, select_patterns


SCENARIOS = [
    {
        "name": "marketing landing baseline",
        "site_type": "marketing-landing",
        "buckets": ["nav", "hero", "card", "stat", "background", "footer"],
        "signals": {
            "has_fixed_nav",
            "has_large_display_heading",
            "expressive_brand",
            "card_grid_present",
            "numeric_stats_present",
            "hero_has_background_layers",
            "footer_present",
        },
        "expect": {
            "nav": "scroll-velocity-navbar",
            "hero": "kinetic-typography-splittext",
            "card": "scroll-trigger-reveal",
            "stat": "number-counter-easing",
            "background": "parallax-depth-layers",
            "footer": "scroll-trigger-reveal",
        },
    },
    {
        "name": "portfolio media-rich baseline",
        "site_type": "portfolio",
        "buckets": ["nav", "hero", "card", "gallery", "timeline", "footer"],
        "signals": {
            "has_fixed_nav",
            "has_large_display_heading",
            "expressive_brand",
            "card_has_media",
            "hover_relevant",
            "gallery_present",
            "timeline_present",
            "footer_present",
        },
        "expect": {
            "nav": "scroll-velocity-navbar",
            "hero": "kinetic-typography-splittext",
            "card": "product-grid-preview-overlay",
            "gallery": "shared-element-gallery-expand",
            "timeline": "pinned-story-panels",
            "footer": "scroll-trigger-reveal",
        },
    },
    {
        "name": "docs blog utility-safe baseline",
        "site_type": "docs-blog",
        "buckets": ["nav", "hero", "card", "tabs", "footer"],
        "signals": {
            "has_fixed_nav",
            "has_active_nav_state",
            "simple_heading",
            "card_grid_present",
            "tabs_present",
            "footer_present",
            "dense_utility_page",
        },
        "expect": {
            "nav": "nav-active-pill-flip",
            "hero": "scroll-trigger-reveal",
            "card": "scroll-trigger-reveal",
            "tabs": "tabs-shared-indicator",
            "footer": "scroll-trigger-reveal",
        },
    },
    {
        "name": "saas app dashboard-safe baseline",
        "site_type": "saas-app",
        "buckets": ["nav", "hero", "card", "stat", "tabs", "form", "footer"],
        "signals": {
            "has_fixed_nav",
            "has_active_nav_state",
            "has_large_display_heading",
            "card_grid_present",
            "numeric_stats_present",
            "tabs_present",
            "form_present",
            "footer_present",
            "dense_utility_page",
        },
        "expect": {
            "nav": "scroll-velocity-navbar",
            "hero": "staggered-word-reveal",
            "card": "scroll-trigger-reveal",
            "stat": "number-counter-easing",
            "tabs": "tabs-shared-indicator",
            "form": "form-focus-cascade",
            "footer": "scroll-trigger-reveal",
        },
    },
]


WATCHLIST_SCENARIOS = [
    {
        "name": "watchlist blocks heavy hero and falls back",
        "site_type": "marketing-landing",
        "buckets": ["hero"],
        "signals": {
            "has_large_display_heading",
            "expressive_brand",
            "accessibility_first_page",
        },
        "expect": {"hero": "staggered-word-reveal"},
    },
    {
        "name": "watchlist blocks decorative badge completely",
        "site_type": "marketing-landing",
        "buckets": ["badge"],
        "signals": {
            "badge_present",
            "expressive_brand",
            "accessibility_first_page",
            "dense_utility_page",
        },
        "expect": {},
    },
]


def main() -> int:
    baselines, watchlist = load_runtime_trend_files()
    failures: list[str] = []
    results: list[dict] = []

    for scenario in SCENARIOS + WATCHLIST_SCENARIOS:
        actual = select_patterns(
            scenario["site_type"],
            scenario["buckets"],
            set(scenario["signals"]),
            baselines,
            watchlist,
        )
        results.append({"name": scenario["name"], "actual": actual})
        if actual != scenario["expect"]:
            failures.append(
                f"{scenario['name']}: expected {scenario['expect']}, got {actual}"
            )

    print(json.dumps({"ok": not failures, "results": results, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
