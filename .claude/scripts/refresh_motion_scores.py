from __future__ import annotations

from collections import OrderedDict
from datetime import date
from importlib.machinery import SourceFileLoader
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
LIB_DIR = ROOT / ".claude" / "motion-library"
CATALOG_PATH = LIB_DIR / "catalog.yaml"
SCORES_PATH = LIB_DIR / "scores.yaml"
OVERVIEW_PATH = LIB_DIR / "trends-overview.md"
GENERATOR_PATH = ROOT / ".claude" / "scripts" / "generate_motion_library.py"

TODAY_MONTH = date.today().strftime("%Y-%m")

GSAP_LLM = "https://gsap.com/llms.txt"
GSAP_SCROLLTRIGGER = "https://gsap.com/docs/v3/Plugins/ScrollTrigger/"
GSAP_SPLITTEXT = "https://gsap.com/docs/v3/Plugins/SplitText/"
GSAP_FLIP = "https://gsap.com/docs/v3/Plugins/Flip/"
GSAP_DRAGGABLE = "https://gsap.com/docs/v3/Plugins/Draggable/"
GSAP_OBSERVER = "https://gsap.com/docs/v3/Plugins/Observer/"
GSAP_MOTIONPATH = "https://gsap.com/docs/v3/Plugins/MotionPathPlugin/"
GSAP_MORPHSVG = "https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/"
GSAP_DRAWSVG = "https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/"
GSAP_SCROLLSMOOTHER = "https://gsap.com/docs/v3/Plugins/ScrollSmoother/"
MDN_CSS_ANIMATIONS = "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations"
MDN_ANIMATION_TIMELINE = "https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline"
MDN_VIEW_TRANSITIONS = "https://developer.mozilla.org/en-US/docs/Web/API/Document/startViewTransition"
MDN_FONT_VARIATIONS = "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variation-settings"
CODROPS_FREE_PLUGINS = "https://tympanus.net/codrops/2025/05/14/from-splittext-to-morphsvg-5-creative-demos-using-free-gsap-plugins/"
CODROPS_PRODUCT_GRID = "https://tympanus.net/codrops/2025/05/27/animated-product-grid-preview-with-gsap-clip-path/"
CODROPS_DRAGGABLE_GRID = "https://tympanus.net/codrops/2025/09/01/recreating-palmers-draggable-product-grid-with-gsap/"
CODROPS_SCROLLSMOOTHER = "https://tympanus.net/codrops/2025/10/29/building-a-layered-zoom-scroll-effect-with-gsap-scrollsmoother-and-scrolltrigger/"
CODROPS_3D_TEXT = "https://tympanus.net/codrops/2025/11/04/creating-3d-scroll-driven-text-animations-with-css-and-gsap/"
CODROPS_CINEMATIC_3D = "https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/"
CODROPS_CURVED_PATH = "https://tympanus.net/codrops/2025/12/17/building-responsive-scroll-triggered-curved-path-animations-with-gsap/"
CODROPS_NITE_RIOT = "https://tympanus.net/codrops/2025/04/15/nite-riot-minimalism-gets-a-wild-side/"

SOURCE_BUNDLES = {
    "scroll": [GSAP_LLM, GSAP_SCROLLTRIGGER, CODROPS_SCROLLSMOOTHER, CODROPS_CURVED_PATH],
    "typography": [GSAP_LLM, GSAP_SPLITTEXT, CODROPS_FREE_PLUGINS, CODROPS_3D_TEXT],
    "ui": [GSAP_LLM, GSAP_FLIP, GSAP_DRAGGABLE, CODROPS_PRODUCT_GRID, CODROPS_DRAGGABLE_GRID],
    "media": [GSAP_LLM, GSAP_FLIP, GSAP_DRAGGABLE, CODROPS_PRODUCT_GRID, CODROPS_DRAGGABLE_GRID],
    "svg": [GSAP_LLM, GSAP_MOTIONPATH, GSAP_MORPHSVG, GSAP_DRAWSVG, CODROPS_FREE_PLUGINS, CODROPS_CURVED_PATH],
    "native": [MDN_ANIMATION_TIMELINE, MDN_VIEW_TRANSITIONS, MDN_FONT_VARIATIONS],
    "css_ui": [MDN_CSS_ANIMATIONS, MDN_VIEW_TRANSITIONS, MDN_FONT_VARIATIONS],
    "cursor": [GSAP_LLM, GSAP_DRAGGABLE, CODROPS_NITE_RIOT, CODROPS_DRAGGABLE_GRID],
    "ambient": [GSAP_LLM, CODROPS_FREE_PLUGINS, CODROPS_NITE_RIOT],
    "observer": [GSAP_LLM, GSAP_OBSERVER, GSAP_SCROLLTRIGGER, CODROPS_SCROLLSMOOTHER],
}

DEFAULT_RULES = {
    "scroll": (8, "trending", "medium", "scroll"),
    "typography": (8, "trending", "medium", "typography"),
    "transition": (8, "trending", "medium", "ui"),
    "micro-interaction": (7, "evergreen", "medium", "ui"),
    "svg": (8, "emerging", "medium", "svg"),
    "cursor": (7, "evergreen", "medium", "cursor"),
    "ambient": (6, "evergreen", "medium", "ambient"),
}

ID_RULES = {
    "scroll-trigger-reveal": (9, "trending", "high", "scroll"),
    "spring-physics-interactions": (9, "trending", "high", "ui"),
    "kinetic-typography-splittext": (9, "trending", "high", "typography"),
    "css-scroll-driven-animations": (8, "emerging", "medium", "native"),
    "morphing-button-states": (7, "evergreen", "medium", "css_ui"),
    "idle-breathing-pulse": (6, "evergreen", "medium", "css_ui"),
    "view-transitions-api": (8, "emerging", "high", "native"),
    "ambient-floating-particles": (5, "declining", "low", "ambient"),
    "card-flip-3d": (4, "declining", "low", "css_ui"),
    "pinned-story-panels": (9, "trending", "high", "scroll"),
    "stacked-cards-scroll-pin": (9, "trending", "high", "scroll"),
    "clip-path-image-wipe-scroll": (9, "trending", "high", "media"),
    "sticky-media-content-sync": (9, "trending", "high", "scroll"),
    "image-sequence-scroll-scrub": (8, "emerging", "medium", "scroll"),
    "zoom-out-hero-exit": (8, "trending", "medium", "scroll"),
    "section-progress-rail": (8, "trending", "medium", "scroll"),
    "scroll-velocity-navbar": (9, "trending", "high", "scroll"),
    "observer-section-slider": (8, "emerging", "medium", "observer"),
    "responsive-curved-path-scroll": (8, "emerging", "medium", "svg"),
    "pinned-hotspot-journey": (8, "trending", "high", "scroll"),
    "scrollsmoother-data-effects": (9, "trending", "high", "scroll"),
    "splittext-line-mask-lift": (9, "trending", "high", "typography"),
    "splittext-char-rotation-burst": (8, "trending", "medium", "typography"),
    "splittext-random-stagger-reveal": (8, "trending", "medium", "typography"),
    "scramble-hover-relabel": (7, "evergreen", "medium", "typography"),
    "svg-clip-mask-text-reveal": (8, "emerging", "medium", "typography"),
    "3d-cylinder-text-scroll": (8, "emerging", "medium", "typography"),
    "circular-text-orbit-scroll": (7, "emerging", "medium", "svg"),
    "text-highlight-sweep": (8, "trending", "medium", "typography"),
    "marker-underline-draw": (8, "trending", "medium", "svg"),
    "odometer-digit-roll": (8, "trending", "medium", "ui"),
    "hamburger-icon-morph": (7, "evergreen", "medium", "ui"),
    "nav-active-pill-flip": (9, "trending", "high", "ui"),
    "mega-menu-stagger-reveal": (8, "trending", "medium", "ui"),
    "accordion-scale-reveal": (8, "trending", "medium", "ui"),
    "tabs-shared-indicator": (9, "trending", "high", "ui"),
    "modal-depth-intro": (8, "trending", "high", "ui"),
    "drawer-spring-slide": (8, "trending", "high", "ui"),
    "toast-stack-dismiss": (8, "trending", "medium", "ui"),
    "tooltip-follow-reveal": (7, "emerging", "medium", "ui"),
    "form-focus-cascade": (8, "trending", "medium", "ui"),
    "draggable-card-deck": (8, "trending", "high", "media"),
    "horizontal-loop-carousel": (8, "trending", "medium", "media"),
    "before-after-drag-reveal": (8, "trending", "high", "media"),
    "cursor-image-preview-trail": (8, "trending", "medium", "media"),
    "product-grid-preview-overlay": (9, "trending", "high", "media"),
    "hover-video-preview-scrub": (8, "emerging", "medium", "media"),
    "shared-element-gallery-expand": (9, "trending", "high", "media"),
    "drag-to-reorder-grid": (8, "emerging", "medium", "media"),
    "stacked-testimonial-rotator": (7, "evergreen", "medium", "media"),
    "orbiting-thumbnail-gallery": (7, "emerging", "medium", "media"),
    "drawsvg-route-reveal": (8, "trending", "medium", "svg"),
    "morphsvg-logo-sequence": (8, "emerging", "medium", "svg"),
    "motionpath-badge-orbit": (8, "emerging", "medium", "svg"),
    "motionpath-cta-journey": (8, "emerging", "medium", "svg"),
    "checkmark-success-morph": (8, "trending", "high", "svg"),
    "gooey-blob-morph": (7, "emerging", "medium", "svg"),
    "radial-icon-burst": (7, "evergreen", "medium", "svg"),
    "orbital-loader-dots": (8, "trending", "medium", "svg"),
    "lenis-smooth-scroll": (7, "evergreen", "medium", "scroll"),
    "horizontal-scroll-section": (8, "evergreen", "medium", "scroll"),
    "marquee-infinite-scroll": (7, "evergreen", "medium", "scroll"),
    "custom-cursor-follower": (7, "evergreen", "medium", "cursor"),
    "magnetic-cursor-pull": (8, "evergreen", "medium", "cursor"),
    "3d-tilt-parallax-cursor": (7, "evergreen", "medium", "cursor"),
    "text-scramble-decode": (7, "evergreen", "medium", "typography"),
    "number-counter-easing": (7, "evergreen", "medium", "ui"),
    "staggered-word-reveal": (8, "evergreen", "medium", "typography"),
    "gradient-text-flow": (6, "evergreen", "medium", "css_ui"),
    "variable-font-morphing": (7, "emerging", "medium", "native"),
    "bento-grid-motion": (8, "evergreen", "high", "media"),
    "flip-layout-animations": (8, "evergreen", "high", "ui"),
    "parallax-depth-layers": (7, "evergreen", "medium", "scroll"),
    "gesture-swipe-animations": (8, "evergreen", "medium", "media"),
    "ripple-wave-click": (6, "evergreen", "medium", "ui"),
}

FIELD_ORDER = [
    "id",
    "name",
    "type",
    "category",
    "framework",
    "triggers",
    "components",
    "folder",
    "snippet",
    "description",
    "trend_score",
    "status",
    "popularity_signal",
    "last_reviewed",
    "sources",
    "manual_override",
    "notes",
]


def load_catalog() -> list[dict]:
    return yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))["patterns"]


def pick_rule(entry: dict, generator) -> tuple[int, str, str, str]:
    if entry["id"] in ID_RULES:
        return ID_RULES[entry["id"]]

    family = generator.infer_family(entry["id"])
    if family in {"observer"}:
        return 8, "emerging", "medium", "observer"
    if family in {"motionpath", "morph", "drawsvg"}:
        return 8, "emerging", "medium", "svg"
    if family in {"draggable", "before_after", "shared_expand", "reorder"}:
        return 8, "trending", "high", "media"
    return DEFAULT_RULES.get(entry["category"], (7, "evergreen", "medium", "ui"))


def ordered_entry(entry: dict) -> OrderedDict:
    return OrderedDict((field, entry[field]) for field in FIELD_ORDER)


def decorate_for_overview(entry: dict, contexts: list[str], generator) -> dict:
    decorated = dict(entry)
    decorated["_contexts"] = contexts
    decorated["_best_for"] = generator.infer_best_for(entry["components"], contexts)
    decorated["_feel"] = generator.infer_feel(entry["category"], generator.infer_family(entry["id"]))
    decorated["_avoid"] = generator.infer_avoid(entry["category"], generator.infer_family(entry["id"]))
    return decorated


def main() -> None:
    generator = SourceFileLoader("motion_library_generator", str(GENERATOR_PATH)).load_module()
    catalog = load_catalog()
    previous = {entry["id"]: (entry.get("trend_score"), entry.get("status")) for entry in catalog}
    old_score_contexts = generator.existing_contexts(generator.current_scores())
    generated_contexts = {entry["id"]: entry["_contexts"] for entry in generator.derive_new_patterns()}

    changed: list[str] = []
    refreshed: list[OrderedDict] = []
    decorated: list[dict] = []

    for entry in catalog:
        updated = dict(entry)
        if not updated.get("manual_override", False):
            score, status, popularity, bundle = pick_rule(updated, generator)
            updated["trend_score"] = score
            updated["status"] = status
            updated["popularity_signal"] = popularity
            updated["last_reviewed"] = TODAY_MONTH
            updated["sources"] = SOURCE_BUNDLES[bundle]
            if status == "declining":
                updated["notes"] = "Retained as a low-priority fallback; dated against the March 2026 GSAP/Codrops baseline."
            else:
                updated["notes"] = "Refreshed against the March 2026 GSAP/Codrops baseline."

        if previous[updated["id"]] != (updated["trend_score"], updated["status"]):
            changed.append(updated["id"])

        contexts = generated_contexts.get(updated["id"], old_score_contexts.get(updated["id"], []))
        decorated.append(decorate_for_overview(updated, contexts, generator))
        refreshed.append(ordered_entry(updated))

    generator.write_catalog(refreshed)
    OVERVIEW_PATH.write_text(generator.overview_markdown(decorated), encoding="utf-8")
    generator.write_scores(refreshed, {entry["id"]: entry["_contexts"] for entry in decorated})

    print(f"Refreshed {len(refreshed)} patterns.")
    print(f"Changed score/status entries: {len(changed)}")
    if changed:
        print("Notable changes:")
        for pattern_id in changed[:12]:
            current = next(entry for entry in refreshed if entry["id"] == pattern_id)
            print(f"- {pattern_id}: {current['trend_score']} / {current['status']}")


if __name__ == "__main__":
    main()
