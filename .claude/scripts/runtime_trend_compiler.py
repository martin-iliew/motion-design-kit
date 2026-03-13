from __future__ import annotations

from collections import OrderedDict
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
LIB_DIR = ROOT / ".claude" / "motion-library"
SITE_BASELINES_PATH = LIB_DIR / "site-baselines.yaml"
TREND_WATCHLIST_PATH = LIB_DIR / "trend-watchlist.yaml"

TODAY = date.today().isoformat()

SITE_BASELINE_RECIPES: OrderedDict[str, OrderedDict[str, list[dict]]] = OrderedDict(
    [
        (
            "marketing-landing",
            OrderedDict(
                [
                    ("nav", [
                        {"pattern": "scroll-velocity-navbar", "when": ["has_fixed_nav"]},
                        {"pattern": "nav-active-pill-flip", "when": ["has_active_nav_state"]},
                    ]),
                    ("hero", [
                        {"pattern": "kinetic-typography-splittext", "when": ["has_large_display_heading", "expressive_brand"]},
                        {"pattern": "staggered-word-reveal", "when": ["has_large_display_heading"]},
                        {"pattern": "scroll-trigger-reveal", "when": ["simple_heading"]},
                    ]),
                    ("badge", [
                        {"pattern": "text-scramble-decode", "when": ["badge_present", "expressive_brand"]},
                        {"pattern": "motionpath-badge-orbit", "when": ["badge_present", "hero_has_background_layers", "expressive_brand"]},
                    ]),
                    ("card", [
                        {"pattern": "product-grid-preview-overlay", "when": ["card_has_media", "hover_relevant"]},
                        {"pattern": "scroll-trigger-reveal", "when": ["card_grid_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["desktop_interaction_ok"]},
                    ]),
                    ("stat", [
                        {"pattern": "number-counter-easing", "when": ["numeric_stats_present"]},
                        {"pattern": "odometer-digit-roll", "when": ["numeric_stats_present", "expressive_brand"]},
                    ]),
                    ("cta", [
                        {"pattern": "morphing-button-states", "when": ["cta_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["cta_present", "desktop_interaction_ok"]},
                        {"pattern": "idle-breathing-pulse", "when": ["cta_present", "expressive_brand"]},
                    ]),
                    ("pricing", [
                        {"pattern": "scroll-trigger-reveal", "when": ["pricing_cards_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["pricing_cards_present", "desktop_interaction_ok"]},
                    ]),
                    ("footer", [
                        {"pattern": "scroll-trigger-reveal", "when": ["footer_present"]},
                    ]),
                    ("tabs", [
                        {"pattern": "tabs-shared-indicator", "when": ["tabs_present"]},
                    ]),
                    ("form", [
                        {"pattern": "form-focus-cascade", "when": ["form_present"]},
                    ]),
                    ("timeline", [
                        {"pattern": "pinned-story-panels", "when": ["timeline_present", "expressive_brand"]},
                        {"pattern": "scroll-trigger-reveal", "when": ["timeline_present"]},
                    ]),
                    ("background", [
                        {"pattern": "parallax-depth-layers", "when": ["hero_has_background_layers"]},
                        {"pattern": "zoom-out-hero-exit", "when": ["hero_has_background_layers", "expressive_brand"]},
                        {"pattern": "scrollsmoother-data-effects", "when": ["hero_has_background_layers", "expressive_brand"]},
                    ]),
                ]
            ),
        ),
        (
            "portfolio",
            OrderedDict(
                [
                    ("nav", [
                        {"pattern": "scroll-velocity-navbar", "when": ["has_fixed_nav"]},
                        {"pattern": "nav-active-pill-flip", "when": ["has_active_nav_state"]},
                        {"pattern": "magnetic-cursor-pull", "when": ["desktop_interaction_ok"]},
                    ]),
                    ("hero", [
                        {"pattern": "kinetic-typography-splittext", "when": ["has_large_display_heading", "expressive_brand"]},
                        {"pattern": "splittext-line-mask-lift", "when": ["has_large_display_heading"]},
                        {"pattern": "staggered-word-reveal", "when": ["simple_heading"]},
                    ]),
                    ("badge", [
                        {"pattern": "motionpath-badge-orbit", "when": ["badge_present", "expressive_brand"]},
                        {"pattern": "text-scramble-decode", "when": ["badge_present"]},
                    ]),
                    ("card", [
                        {"pattern": "product-grid-preview-overlay", "when": ["card_has_media", "hover_relevant"]},
                        {"pattern": "scroll-trigger-reveal", "when": ["card_grid_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["desktop_interaction_ok"]},
                    ]),
                    ("gallery", [
                        {"pattern": "shared-element-gallery-expand", "when": ["gallery_present"]},
                        {"pattern": "hover-video-preview-scrub", "when": ["gallery_present", "hover_relevant"]},
                        {"pattern": "before-after-drag-reveal", "when": ["gallery_present", "card_has_media"]},
                    ]),
                    ("cta", [
                        {"pattern": "spring-physics-interactions", "when": ["cta_present", "desktop_interaction_ok"]},
                        {"pattern": "morphing-button-states", "when": ["cta_present"]},
                    ]),
                    ("footer", [
                        {"pattern": "scroll-trigger-reveal", "when": ["footer_present"]},
                    ]),
                    ("timeline", [
                        {"pattern": "pinned-story-panels", "when": ["timeline_present", "expressive_brand"]},
                        {"pattern": "sticky-media-content-sync", "when": ["timeline_present", "card_has_media"]},
                        {"pattern": "stacked-cards-scroll-pin", "when": ["timeline_present", "card_grid_present"]},
                    ]),
                    ("background", [
                        {"pattern": "parallax-depth-layers", "when": ["hero_has_background_layers"]},
                        {"pattern": "scrollsmoother-data-effects", "when": ["hero_has_background_layers", "expressive_brand"]},
                    ]),
                ]
            ),
        ),
        (
            "docs-blog",
            OrderedDict(
                [
                    ("nav", [
                        {"pattern": "nav-active-pill-flip", "when": ["has_active_nav_state"]},
                        {"pattern": "scroll-velocity-navbar", "when": ["has_fixed_nav"]},
                    ]),
                    ("hero", [
                        {"pattern": "scroll-trigger-reveal", "when": ["simple_heading"]},
                        {"pattern": "staggered-word-reveal", "when": ["has_large_display_heading"]},
                    ]),
                    ("card", [
                        {"pattern": "scroll-trigger-reveal", "when": ["card_grid_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["desktop_interaction_ok", "hover_relevant"]},
                    ]),
                    ("cta", [
                        {"pattern": "morphing-button-states", "when": ["cta_present"]},
                    ]),
                    ("footer", [
                        {"pattern": "scroll-trigger-reveal", "when": ["footer_present"]},
                    ]),
                    ("tabs", [
                        {"pattern": "tabs-shared-indicator", "when": ["tabs_present"]},
                    ]),
                    ("form", [
                        {"pattern": "form-focus-cascade", "when": ["form_present"]},
                    ]),
                    ("timeline", [
                        {"pattern": "scroll-trigger-reveal", "when": ["timeline_present"]},
                    ]),
                ]
            ),
        ),
        (
            "ecommerce",
            OrderedDict(
                [
                    ("nav", [
                        {"pattern": "scroll-velocity-navbar", "when": ["has_fixed_nav"]},
                        {"pattern": "nav-active-pill-flip", "when": ["has_active_nav_state"]},
                    ]),
                    ("hero", [
                        {"pattern": "scroll-trigger-reveal", "when": ["simple_heading"]},
                        {"pattern": "staggered-word-reveal", "when": ["has_large_display_heading"]},
                    ]),
                    ("card", [
                        {"pattern": "product-grid-preview-overlay", "when": ["card_has_media", "hover_relevant"]},
                        {"pattern": "scroll-trigger-reveal", "when": ["card_grid_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["desktop_interaction_ok"]},
                    ]),
                    ("gallery", [
                        {"pattern": "shared-element-gallery-expand", "when": ["gallery_present"]},
                        {"pattern": "before-after-drag-reveal", "when": ["gallery_present", "card_has_media"]},
                        {"pattern": "hover-video-preview-scrub", "when": ["gallery_present", "hover_relevant"]},
                    ]),
                    ("cta", [
                        {"pattern": "morphing-button-states", "when": ["cta_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["cta_present", "desktop_interaction_ok"]},
                    ]),
                    ("pricing", [
                        {"pattern": "scroll-trigger-reveal", "when": ["pricing_cards_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["pricing_cards_present", "desktop_interaction_ok"]},
                    ]),
                    ("stat", [
                        {"pattern": "number-counter-easing", "when": ["numeric_stats_present"]},
                    ]),
                    ("form", [
                        {"pattern": "form-focus-cascade", "when": ["form_present"]},
                    ]),
                    ("footer", [
                        {"pattern": "scroll-trigger-reveal", "when": ["footer_present"]},
                    ]),
                    ("background", [
                        {"pattern": "parallax-depth-layers", "when": ["hero_has_background_layers"]},
                    ]),
                ]
            ),
        ),
        (
            "saas-app",
            OrderedDict(
                [
                    ("nav", [
                        {"pattern": "scroll-velocity-navbar", "when": ["has_fixed_nav"]},
                        {"pattern": "nav-active-pill-flip", "when": ["has_active_nav_state"]},
                    ]),
                    ("hero", [
                        {"pattern": "staggered-word-reveal", "when": ["has_large_display_heading"]},
                        {"pattern": "scroll-trigger-reveal", "when": ["simple_heading"]},
                        {"pattern": "kinetic-typography-splittext", "when": ["has_large_display_heading", "expressive_brand"]},
                    ]),
                    ("card", [
                        {"pattern": "scroll-trigger-reveal", "when": ["card_grid_present"]},
                        {"pattern": "spring-physics-interactions", "when": ["desktop_interaction_ok"]},
                        {"pattern": "bento-grid-motion", "when": ["card_grid_present"]},
                    ]),
                    ("stat", [
                        {"pattern": "number-counter-easing", "when": ["numeric_stats_present"]},
                        {"pattern": "odometer-digit-roll", "when": ["numeric_stats_present", "expressive_brand"]},
                    ]),
                    ("tabs", [
                        {"pattern": "tabs-shared-indicator", "when": ["tabs_present"]},
                    ]),
                    ("form", [
                        {"pattern": "form-focus-cascade", "when": ["form_present"]},
                    ]),
                    ("cta", [
                        {"pattern": "morphing-button-states", "when": ["cta_present"]},
                    ]),
                    ("footer", [
                        {"pattern": "scroll-trigger-reveal", "when": ["footer_present"]},
                    ]),
                    ("timeline", [
                        {"pattern": "scroll-trigger-reveal", "when": ["timeline_present"]},
                    ]),
                    ("background", [
                        {"pattern": "parallax-depth-layers", "when": ["hero_has_background_layers", "expressive_brand"]},
                    ]),
                ]
            ),
        ),
    ]
)

WATCHLIST_PATTERNS: OrderedDict[str, dict] = OrderedDict(
    [
        (
            "kinetic-typography-splittext",
            {
                "avoid_when": ["simple_heading", "accessibility_first_page", "dense_utility_page"],
                "notes": "Use only when the hero is visually dominant and can carry heavier text treatment.",
            },
        ),
        (
            "splittext-line-mask-lift",
            {
                "avoid_when": ["accessibility_first_page", "dense_utility_page"],
                "notes": "Prefer on expressive portfolio hero copy, not on dense reading surfaces.",
            },
        ),
        (
            "text-scramble-decode",
            {
                "avoid_when": ["accessibility_first_page", "dense_utility_page"],
                "notes": "Reserve for short decorative labels rather than informational copy.",
            },
        ),
        (
            "custom-cursor-follower",
            {
                "avoid_when": ["non_portfolio_page", "touch_heavy_audience", "accessibility_first_page"],
                "notes": "Do not apply on standard marketing, docs, or touch-led experiences.",
            },
        ),
        (
            "magnetic-cursor-pull",
            {
                "avoid_when": ["touch_heavy_audience", "accessibility_first_page"],
                "notes": "Cursor-led pull interactions should stay desktop-only and opt-in.",
            },
        ),
        (
            "ambient-floating-particles",
            {
                "avoid_when": ["non_expressive_brand", "dense_utility_page", "accessibility_first_page"],
                "notes": "Only for premium atmospheric hero sections where motion can stay subordinate to content.",
            },
        ),
        (
            "scrollsmoother-data-effects",
            {
                "avoid_when": ["dense_utility_page", "accessibility_first_page"],
                "notes": "Use on premium storytelling shells only, never on dense utility or accessibility-first pages.",
            },
        ),
        (
            "flip-layout-animations",
            {
                "avoid_when": ["dense_utility_page", "accessibility_first_page"],
                "notes": "Avoid when stable layout predictability matters more than spectacle.",
            },
        ),
        (
            "pinned-story-panels",
            {
                "avoid_when": ["dense_utility_page", "accessibility_first_page"],
                "notes": "Pinned sequences should not interrupt utilitarian reading or task flows.",
            },
        ),
        (
            "stacked-cards-scroll-pin",
            {
                "avoid_when": ["dense_utility_page", "accessibility_first_page"],
                "notes": "Use only when the page can afford scroll-driven choreography.",
            },
        ),
        (
            "motionpath-badge-orbit",
            {
                "avoid_when": ["dense_utility_page", "accessibility_first_page"],
                "notes": "Orbiting badges are decorative and should stay out of utilitarian layouts.",
            },
        ),
        (
            "shared-element-gallery-expand",
            {
                "avoid_when": ["accessibility_first_page"],
                "notes": "Only use when the gallery meaningfully benefits from an expanded immersive state.",
            },
        ),
    ]
)


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _catalog_by_id(catalog_patterns: list[dict]) -> dict[str, dict]:
    return {entry["id"]: entry for entry in catalog_patterns}


def build_site_baselines(catalog_patterns: list[dict]) -> dict:
    catalog = _catalog_by_id(catalog_patterns)
    payload: dict[str, dict] = {"site_baselines": {}}

    for site_type, buckets in SITE_BASELINE_RECIPES.items():
        payload["site_baselines"][site_type] = {}
        for bucket, candidates in buckets.items():
            compiled = []
            for candidate in candidates:
                entry = catalog.get(candidate["pattern"])
                if not entry or entry.get("status") == "declining":
                    continue
                compiled.append(
                    {
                        "pattern": candidate["pattern"],
                        "when": candidate.get("when", []),
                    }
                )
                if len(compiled) == 3:
                    break
            if compiled:
                payload["site_baselines"][site_type][bucket] = compiled
    return payload


def build_trend_watchlist(catalog_patterns: list[dict]) -> dict:
    catalog = _catalog_by_id(catalog_patterns)
    payload = {"watchlist": {"patterns": {}}}

    for pattern_id, rule in WATCHLIST_PATTERNS.items():
        if pattern_id not in catalog:
            continue
        payload["watchlist"]["patterns"][pattern_id] = {
            "avoid_when": rule.get("avoid_when", []),
            "notes": rule.get("notes", ""),
        }
    return payload


def _with_header(title: str, generated_from: str, data: dict) -> str:
    yaml_body = yaml.safe_dump(data, sort_keys=False, allow_unicode=False)
    return "\n".join(
        [
            title,
            "# AUTO-GENERATED by .claude/scripts/refresh_motion_scores.py -- do not edit manually",
            f"# Generated from: {generated_from}",
            f"# Last updated: {TODAY}",
            "",
            yaml_body,
        ]
    )


def write_runtime_trend_files(catalog_patterns: list[dict]) -> tuple[dict, dict]:
    baselines = build_site_baselines(catalog_patterns)
    watchlist = build_trend_watchlist(catalog_patterns)

    SITE_BASELINES_PATH.write_text(
        _with_header(
            "# runtime site-type -> bucket -> ranked candidates",
            "catalog.yaml + scores.yaml + trends-overview.md",
            baselines,
        ),
        encoding="utf-8",
    )
    TREND_WATCHLIST_PATH.write_text(
        _with_header(
            "# runtime watchlist -> pattern -> avoid rules",
            "catalog.yaml + trends-overview.md",
            watchlist,
        ),
        encoding="utf-8",
    )
    return baselines, watchlist


def load_runtime_trend_files() -> tuple[dict, dict]:
    return _load_yaml(SITE_BASELINES_PATH), _load_yaml(TREND_WATCHLIST_PATH)


def select_patterns(
    site_type: str,
    detected_buckets: list[str],
    active_signals: set[str],
    baselines: dict,
    watchlist: dict,
) -> dict[str, str]:
    chosen: dict[str, str] = {}
    site_baselines = baselines.get("site_baselines", {}).get(site_type, {})
    blocked = watchlist.get("watchlist", {}).get("patterns", {})

    for bucket in detected_buckets:
        for candidate in site_baselines.get(bucket, []):
            required = set(candidate.get("when", []))
            if not required.issubset(active_signals):
                continue
            avoid = set(blocked.get(candidate["pattern"], {}).get("avoid_when", []))
            if avoid & active_signals:
                continue
            chosen[bucket] = candidate["pattern"]
            break
    return chosen


def validate_runtime_payloads(catalog_patterns: list[dict], baselines: dict, watchlist: dict) -> list[str]:
    issues: list[str] = []
    catalog = _catalog_by_id(catalog_patterns)

    site_baselines = baselines.get("site_baselines", {})
    required_sites = set(SITE_BASELINE_RECIPES.keys())
    if set(site_baselines.keys()) != required_sites:
        issues.append("site-baselines.yaml does not contain the expected site types")

    for site_type, buckets in site_baselines.items():
        if not isinstance(buckets, dict):
            issues.append(f"site-baselines {site_type} is not a mapping")
            continue
        for bucket, candidates in buckets.items():
            if len(candidates) > 3:
                issues.append(f"site-baselines {site_type}.{bucket} has more than 3 candidates")
            for candidate in candidates:
                pattern_id = candidate.get("pattern")
                if pattern_id not in catalog:
                    issues.append(f"site-baselines {site_type}.{bucket} references unknown pattern {pattern_id}")
                    continue
                if catalog[pattern_id].get("status") == "declining":
                    issues.append(f"site-baselines {site_type}.{bucket} includes declining pattern {pattern_id}")
                if "when" not in candidate or not isinstance(candidate["when"], list):
                    issues.append(f"site-baselines {site_type}.{bucket}.{pattern_id} is missing a when list")

    patterns = watchlist.get("watchlist", {}).get("patterns", {})
    for pattern_id, rule in patterns.items():
        if pattern_id not in catalog:
            issues.append(f"trend-watchlist references unknown pattern {pattern_id}")
            continue
        if "avoid_when" not in rule or not isinstance(rule["avoid_when"], list):
            issues.append(f"trend-watchlist {pattern_id} is missing an avoid_when list")

    return issues
