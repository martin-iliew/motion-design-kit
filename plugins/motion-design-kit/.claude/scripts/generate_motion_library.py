from __future__ import annotations

from collections import OrderedDict, defaultdict
from copy import deepcopy
from datetime import date
from pathlib import Path
import re
import textwrap

import yaml


ROOT = Path(__file__).resolve().parents[2]
LIB_DIR = ROOT / ".claude" / "motion-library"
CATALOG_PATH = LIB_DIR / "catalog.yaml"
SCORES_PATH = LIB_DIR / "scores.yaml"
OVERVIEW_PATH = LIB_DIR / "trends-overview.md"

TODAY = date.today()
TODAY_DAY = TODAY.isoformat()
TODAY_MONTH = TODAY.strftime("%Y-%m")
SITE_CONTEXTS = ["saas", "portfolio", "marketing", "dashboard", "ecommerce", "creative"]
CATEGORY_ORDER = ["scroll", "typography", "micro-interaction", "transition", "cursor", "ambient", "svg"]

URLS = {
    "llms": "https://gsap.com/llms.txt",
    "scrolltrigger": "https://gsap.com/docs/v3/Plugins/ScrollTrigger/",
    "splittext": "https://gsap.com/docs/v3/Plugins/SplitText/",
    "flip": "https://gsap.com/docs/v3/Plugins/Flip/",
    "draggable": "https://gsap.com/docs/v3/Plugins/Draggable/",
    "observer": "https://gsap.com/docs/v3/Plugins/Observer/",
    "motionpath": "https://gsap.com/docs/v3/Plugins/MotionPathPlugin/",
    "morphsvg": "https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/",
    "drawsvg": "https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/",
    "scrollsmoother": "https://gsap.com/docs/v3/Plugins/ScrollSmoother/",
    "scramble": "https://gsap.com/docs/v3/Plugins/ScrambleTextPlugin/",
    "codrops": "https://tympanus.net/codrops/",
}

BATCHES = [
    {
        "category": "scroll",
        "framework": "GSAP",
        "triggers": ["scroll", "scroll-enter", "page-load"],
        "components": ["hero", "section", "media", "timeline", "progress-bar", "nav", "hotspot"],
        "ids": [
            "pinned-story-panels",
            "stacked-cards-scroll-pin",
            "clip-path-image-wipe-scroll",
            "sticky-media-content-sync",
            "image-sequence-scroll-scrub",
            "zoom-out-hero-exit",
            "section-progress-rail",
            "scroll-velocity-navbar",
            "observer-section-slider",
            "responsive-curved-path-scroll",
            "pinned-hotspot-journey",
            "scrollsmoother-data-effects",
        ],
    },
    {
        "category": "typography",
        "framework": "GSAP",
        "triggers": ["page-load", "scroll-enter", "hover"],
        "components": ["heading", "text", "label", "badge", "hero"],
        "ids": [
            "splittext-line-mask-lift",
            "splittext-char-rotation-burst",
            "splittext-random-stagger-reveal",
            "scramble-hover-relabel",
            "svg-clip-mask-text-reveal",
            "3d-cylinder-text-scroll",
            "circular-text-orbit-scroll",
            "text-highlight-sweep",
            "marker-underline-draw",
            "odometer-digit-roll",
        ],
    },
    {
        "category": "transition",
        "framework": "GSAP",
        "triggers": ["click", "hover", "focus", "state-change"],
        "components": ["nav", "menu", "tabs", "accordion", "modal", "drawer", "toast", "tooltip", "form", "input", "button"],
        "ids": [
            "hamburger-icon-morph",
            "nav-active-pill-flip",
            "mega-menu-stagger-reveal",
            "accordion-scale-reveal",
            "tabs-shared-indicator",
            "modal-depth-intro",
            "drawer-spring-slide",
            "toast-stack-dismiss",
            "tooltip-follow-reveal",
            "form-focus-cascade",
        ],
    },
    {
        "category": "micro-interaction",
        "framework": "GSAP",
        "triggers": ["drag", "hover", "click", "cursor-move"],
        "components": ["gallery", "carousel", "card", "grid", "media", "image", "video", "testimonial"],
        "ids": [
            "draggable-card-deck",
            "horizontal-loop-carousel",
            "before-after-drag-reveal",
            "cursor-image-preview-trail",
            "product-grid-preview-overlay",
            "hover-video-preview-scrub",
            "shared-element-gallery-expand",
            "drag-to-reorder-grid",
            "stacked-testimonial-rotator",
            "orbiting-thumbnail-gallery",
        ],
    },
    {
        "category": "svg",
        "framework": "GSAP",
        "triggers": ["page-load", "scroll", "hover", "click"],
        "components": ["svg", "icon", "logo", "loader", "badge", "cta", "path"],
        "ids": [
            "drawsvg-route-reveal",
            "morphsvg-logo-sequence",
            "motionpath-badge-orbit",
            "motionpath-cta-journey",
            "checkmark-success-morph",
            "gooey-blob-morph",
            "radial-icon-burst",
            "orbital-loader-dots",
        ],
    },
]

KEYWORD_COMPONENTS = OrderedDict(
    [
        ("story", ["timeline", "section"]),
        ("pinned", ["timeline", "section"]),
        ("stacked", ["timeline", "section"]),
        ("sticky", ["timeline", "section", "media"]),
        ("navbar", ["nav"]),
        ("nav", ["nav"]),
        ("menu", ["menu", "nav"]),
        ("tabs", ["tabs", "menu"]),
        ("accordion", ["accordion"]),
        ("modal", ["modal"]),
        ("drawer", ["drawer"]),
        ("toast", ["toast"]),
        ("tooltip", ["tooltip"]),
        ("form", ["form", "input"]),
        ("input", ["input", "form"]),
        ("gallery", ["gallery", "media", "image"]),
        ("carousel", ["carousel", "gallery"]),
        ("video", ["video", "media"]),
        ("image", ["image", "media"]),
        ("media", ["media"]),
        ("card", ["card"]),
        ("grid", ["grid", "card"]),
        ("testimonial", ["testimonial", "card"]),
        ("hero", ["hero"]),
        ("section", ["section"]),
        ("timeline", ["timeline"]),
        ("progress", ["progress-bar"]),
        ("hotspot", ["hotspot"]),
        ("heading", ["heading", "text"]),
        ("text", ["text"]),
        ("label", ["label"]),
        ("badge", ["badge"]),
        ("logo", ["logo", "icon"]),
        ("icon", ["icon"]),
        ("loader", ["loader", "icon"]),
        ("svg", ["svg"]),
        ("path", ["path", "svg"]),
        ("cta", ["cta", "button"]),
        ("button", ["button"]),
    ]
)

SITE_CONTEXT_OVERRIDES = OrderedDict(
    [
        ("saas", {"personality": "energetic", "avoid": ["card-flip-3d", "ambient-floating-particles"], "prefer": ["tabs-shared-indicator", "section-progress-rail"]}),
        ("portfolio", {"personality": "dramatic", "prefer": ["custom-cursor-follower", "3d-tilt-parallax-cursor", "pinned-story-panels"]}),
        ("marketing", {"personality": "energetic", "prefer": ["kinetic-typography-splittext", "gradient-text-flow", "zoom-out-hero-exit"]}),
        ("dashboard", {"personality": "professional", "prefer": ["number-counter-easing", "tabs-shared-indicator", "toast-stack-dismiss"]}),
        ("ecommerce", {"personality": "subtle", "prefer": ["spring-physics-interactions", "shared-element-gallery-expand", "before-after-drag-reveal"]}),
        ("creative", {"personality": "dramatic", "prefer": ["custom-cursor-follower", "ambient-floating-particles", "morphsvg-logo-sequence"]}),
    ]
)


def kebab_to_title(value: str) -> str:
    special = {"svg": "SVG", "cta": "CTA", "3d": "3D", "gsap": "GSAP", "flip": "FLIP", "drawsvg": "DrawSVG", "morphsvg": "MorphSVG", "scrollsmoother": "ScrollSmoother", "splittext": "SplitText"}
    return " ".join(special.get(part, part.capitalize()) for part in value.split("-"))


def dedupe(items):
    seen = set()
    result = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def plain(value):
    if isinstance(value, OrderedDict):
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [plain(item) for item in value]
    return value


def infer_components(pattern_id: str, batch: dict) -> list[str]:
    picked = []
    for token, components in KEYWORD_COMPONENTS.items():
        if token in pattern_id:
            picked.extend(components)
    if not picked:
        picked.extend(batch["components"][:2])
    filtered = [component for component in dedupe(picked) if component in batch["components"]]
    return filtered or batch["components"][:2]


def infer_contexts(pattern_id: str, components: list[str], category: str) -> list[str]:
    contexts = []
    if {"nav", "menu", "tabs", "accordion", "modal", "drawer", "toast", "tooltip", "form", "input"} & set(components):
        contexts.extend(["saas", "dashboard", "ecommerce"])
    if {"gallery", "card", "media", "image", "video", "testimonial"} & set(components):
        contexts.extend(["portfolio", "ecommerce", "creative", "marketing"])
    if {"hero", "section", "timeline", "hotspot"} & set(components):
        contexts.extend(["marketing", "portfolio", "creative", "saas"])
    if {"svg", "icon", "logo", "badge", "cta", "path"} & set(components):
        contexts.extend(["creative", "marketing", "portfolio"])
    if category == "typography":
        contexts.extend(["marketing", "portfolio", "creative"])
    return dedupe(contexts)[:4]


def infer_family(pattern_id: str) -> str:
    if "scrollsmoother" in pattern_id:
        return "scrollsmoother"
    if "observer" in pattern_id:
        return "observer"
    if "velocity-navbar" in pattern_id:
        return "nav_velocity"
    if "progress" in pattern_id:
        return "progress"
    if "image-sequence" in pattern_id:
        return "image_sequence"
    if any(token in pattern_id for token in ["motionpath", "orbit", "curved-path"]):
        return "motionpath"
    if "splittext-line" in pattern_id:
        return "splittext_lines"
    if "splittext-char" in pattern_id:
        return "splittext_chars"
    if "splittext-random" in pattern_id:
        return "splittext_random"
    if "scramble" in pattern_id:
        return "scramble"
    if any(token in pattern_id for token in ["underline", "drawsvg"]):
        return "drawsvg"
    if any(token in pattern_id for token in ["highlight", "clip-mask"]):
        return "mask"
    if "odometer" in pattern_id:
        return "odometer"
    if any(token in pattern_id for token in ["hamburger", "checkmark"]):
        return "toggle"
    if any(token in pattern_id for token in ["pill-flip", "shared-indicator"]):
        return "flip_indicator"
    if "accordion" in pattern_id:
        return "accordion"
    if any(token in pattern_id for token in ["mega-menu", "modal", "drawer", "preview-overlay"]):
        return "panel"
    if "toast" in pattern_id:
        return "toast"
    if "tooltip" in pattern_id:
        return "tooltip"
    if "form-focus" in pattern_id:
        return "form_focus"
    if "draggable-card-deck" in pattern_id:
        return "draggable"
    if "loop-carousel" in pattern_id:
        return "loop"
    if "before-after" in pattern_id:
        return "before_after"
    if "cursor-image-preview" in pattern_id:
        return "cursor_preview"
    if "video-preview" in pattern_id:
        return "video_scrub"
    if "shared-element" in pattern_id:
        return "shared_expand"
    if "reorder-grid" in pattern_id:
        return "reorder"
    if "testimonial-rotator" in pattern_id:
        return "stack"
    if any(token in pattern_id for token in ["morphsvg", "gooey"]):
        return "morph"
    if "radial-icon-burst" in pattern_id:
        return "burst"
    if "loader" in pattern_id:
        return "loader"
    if any(token in pattern_id for token in ["pinned", "stacked", "sticky"]):
        return "pin"
    return "scrub"


def infer_type(pattern_id: str, family: str) -> str:
    if family in {"observer", "scrollsmoother", "draggable", "before_after", "cursor_preview", "video_scrub", "morph", "loader", "motionpath"}:
        return "procedural"
    if "scroll-driven" in pattern_id:
        return "browser-native"
    return "tween"


def infer_sources(pattern_id: str, family: str, category: str) -> list[str]:
    tags = ["llms"]
    if category == "scroll":
        tags.append("scrolltrigger")
    if family.startswith("splittext"):
        tags.append("splittext")
    if family == "scramble":
        tags.append("scramble")
    if family in {"flip_indicator", "shared_expand", "reorder", "toast", "stack"}:
        tags.append("flip")
    if family in {"draggable", "loop", "before_after", "reorder"}:
        tags.append("draggable")
    if family == "observer":
        tags.append("observer")
    if family == "motionpath":
        tags.append("motionpath")
    if family == "morph":
        tags.append("morphsvg")
    if family == "drawsvg":
        tags.append("drawsvg")
    if family == "scrollsmoother":
        tags.append("scrollsmoother")
    tags.append("codrops")
    return dedupe(URLS[tag] for tag in tags if tag in URLS)


def infer_description(pattern_id: str, family: str, components: list[str]) -> str:
    component_text = ", ".join(component.replace("-", " ") for component in components[:3])
    phrases = {
        "pin": "pins a sequence and hands focus from one beat to the next as the user scrolls",
        "scrub": "scrubs transform-led motion against scroll without breaking layout",
        "nav_velocity": "uses scroll direction and velocity to tune navigation behavior",
        "observer": "turns section changes into an Observer-driven presentation flow",
        "scrollsmoother": "adds premium smooth-scrolling effects around a GSAP page shell",
        "splittext_lines": "reveals display copy line-by-line with SplitText masking",
        "splittext_chars": "animates characters with dimensional rotation before settling into readable copy",
        "splittext_random": "uses randomized text staggering for a less templated reveal cadence",
        "scramble": "scrambles short labels before resolving to the final copy",
        "mask": "reveals content through a crisp transform-led mask sweep",
        "drawsvg": "draws a path or underline progressively to guide the eye",
        "odometer": "rolls digits mechanically so value changes feel tangible",
        "toggle": "confirms a binary state change with a compact icon morph",
        "flip_indicator": "uses FLIP continuity so active-state indicators glide instead of jump",
        "panel": "stages a panel or overlay with coordinated depth and stagger",
        "accordion": "reveals disclosure content without the hard jump of instant height changes",
        "toast": "keeps stacked notifications organized through entry and dismissal motion",
        "tooltip": "lets hover help text follow the cursor with low-latency motion",
        "form_focus": "cascades adjacent form elements so focus feels guided instead of abrupt",
        "draggable": "makes a deck behave like a direct-manipulation object",
        "loop": "creates a seamless loop for horizontally repeated content",
        "before_after": "lets a draggable handle reveal two media states inside one frame",
        "cursor_preview": "uses cursor-proximate previews to enrich browsing without a click",
        "video_scrub": "scrubs short video previews on hover for richer media cards",
        "shared_expand": "expands a shared element while preserving spatial continuity",
        "reorder": "reflows a grid smoothly around direct drag-based reordering",
        "stack": "rotates stacked cards while preserving depth and order",
        "motionpath": "moves an accent or media element along a defined path",
        "morph": "morphs SVG shapes through a branded sequence",
        "burst": "uses a quick radial burst for celebratory micro-feedback",
        "loader": "keeps asynchronous waiting states alive with orbital motion",
        "image_sequence": "steps through prepared frames so scroll behaves like a lightweight film strip",
        "progress": "builds scoped progress feedback that grows with the reading path",
    }
    return f"{kebab_to_title(pattern_id)} is a GSAP pattern for {component_text} surfaces that {phrases.get(family, 'adds structured motion without relying on layout properties')}."


def infer_best_for(components: list[str], contexts: list[str]) -> str:
    labels = {
        "saas": "SaaS product sections",
        "portfolio": "portfolio storytelling",
        "marketing": "marketing launches",
        "dashboard": "dashboard states",
        "ecommerce": "ecommerce conversion surfaces",
        "creative": "creative showcase pages",
    }
    context_text = ", ".join(labels[context] for context in contexts[:3]) if contexts else "high-value UI moments"
    component_text = ", ".join(component.replace("-", " ") for component in components[:3])
    return f"{context_text} that need clearer motion hierarchy across {component_text} surfaces."


def infer_feel(category: str, family: str) -> str:
    if family in {"pin", "scrub", "image_sequence", "progress"}:
        return "Scroll-coupled and intentional; the motion should track reading pace instead of hijacking it."
    if category == "typography":
        return "Editorial and legible; the flourish should resolve into readable type quickly."
    if family in {"toggle", "panel", "accordion", "toast", "form_focus"}:
        return "State-driven and tactile; movement should confirm the change in one controlled beat."
    if family in {"draggable", "before_after", "reorder", "cursor_preview"}:
        return "Direct-manipulation first; the motion should feel physical without fighting the user."
    if category == "svg":
        return "Branded and sculpted; path or shape motion should feel deliberate, not decorative filler."
    return "Deliberate and lightweight; the motion should add hierarchy before it adds spectacle."


def infer_avoid(category: str, family: str) -> str:
    if family in {"pin", "observer", "scrollsmoother"}:
        return "Dense utility pages, long legal copy, or contexts where native scrolling must stay untouched."
    if category == "typography":
        return "Long-form body copy, dense instructional text, or layouts already carrying multiple text treatments."
    if family in {"draggable", "before_after", "reorder"}:
        return "Critical data surfaces or any flow where accidental drag would hurt basic usability."
    if family in {"toggle", "toast", "tooltip"}:
        return "Passive decoration on non-interactive UI or alerts that need instant, utilitarian clarity."
    return "Low-value surfaces where the effect would add novelty but not clarity."


def infer_score_status(pattern_id: str, family: str) -> tuple[int, str, str]:
    if family in {"pin", "nav_velocity", "flip_indicator", "shared_expand", "scrollsmoother"}:
        return 9, "trending", "high"
    if family in {"observer", "motionpath", "morph", "image_sequence"}:
        return 8, "emerging", "medium"
    if family in {"loader", "drawsvg", "panel", "draggable", "before_after"}:
        return 8, "trending", "high"
    return 8, "trending", "medium"


def current_catalog_patterns():
    return load_yaml(CATALOG_PATH)["patterns"]


def current_scores():
    return load_yaml(SCORES_PATH)


def existing_contexts(scores):
    mapping = defaultdict(set)
    for bucket, contexts in scores.items():
        if bucket == "site_contexts" or not isinstance(contexts, dict):
            continue
        for context, pattern_ids in contexts.items():
            if context == "any":
                continue
            for pattern_id in pattern_ids:
                mapping[pattern_id].add(context)
    return {pattern_id: sorted(contexts) for pattern_id, contexts in mapping.items()}


def normalize_existing_patterns():
    catalog = current_catalog_patterns()
    contexts = existing_contexts(current_scores())
    normalized = []
    seen = set()
    for entry in catalog:
        if entry["id"] in seen:
            continue
        seen.add(entry["id"])
        entry = deepcopy(entry)
        entry["description"] = entry.get("description") or f"{entry['framework']}-based {entry['category'].replace('-', ' ')} pattern for {', '.join(entry['components'][:3])} surfaces."
        entry["sources"] = entry.get("sources") or infer_sources(entry["id"], infer_family(entry["id"]), entry["category"])
        entry["notes"] = entry.get("notes") or "Backfilled description and sources during the March 2026 expansion."
        entry["_contexts"] = contexts.get(entry["id"], [])
        entry["_best_for"] = infer_best_for(entry["components"], entry["_contexts"])
        entry["_feel"] = infer_feel(entry["category"], infer_family(entry["id"]))
        entry["_avoid"] = infer_avoid(entry["category"], infer_family(entry["id"]))
        normalized.append(entry)
    return normalized


def derive_new_patterns():
    patterns = []
    for batch in BATCHES:
        for pattern_id in batch["ids"]:
            family = infer_family(pattern_id)
            components = infer_components(pattern_id, batch)
            contexts = infer_contexts(pattern_id, components, batch["category"])
            score, status, popularity = infer_score_status(pattern_id, family)
            patterns.append(
                {
                    "id": pattern_id,
                    "name": kebab_to_title(pattern_id),
                    "type": infer_type(pattern_id, family),
                    "category": batch["category"],
                    "framework": batch["framework"],
                    "triggers": batch["triggers"],
                    "components": components,
                    "folder": pattern_id,
                    "snippet": "snippet.js",
                    "description": infer_description(pattern_id, family, components),
                    "trend_score": score,
                    "status": status,
                    "popularity_signal": popularity,
                    "last_reviewed": TODAY_MONTH,
                    "sources": infer_sources(pattern_id, family, batch["category"]),
                    "manual_override": False,
                    "notes": "Generated from the March 2026 motion-library expansion generator.",
                    "_family": family,
                    "_contexts": contexts,
                    "_best_for": infer_best_for(components, contexts),
                    "_feel": infer_feel(batch["category"], family),
                    "_avoid": infer_avoid(batch["category"], family),
                }
            )
    return patterns


def js_wrapper(body: str, clear_selector: str, plugins: list[str] | None = None) -> str:
    lines = []
    if plugins:
        lines.append(f"gsap.registerPlugin({', '.join(plugins)});")
    lines.append("const mm = gsap.matchMedia();")
    lines.append('mm.add("(prefers-reduced-motion: no-preference)", () => {')
    lines.append(textwrap.indent(textwrap.dedent(body).strip(), "  "))
    lines.append("});")
    lines.append('mm.add("(prefers-reduced-motion: reduce)", () => {')
    lines.append(f'  gsap.set("{clear_selector}", {{ clearProps: "all" }});')
    lines.append("});")
    return "\n".join(lines) + "\n"


def root_selector(pattern_id: str) -> str:
    return f'[data-motion="{pattern_id}"]'


def snippet_for(pattern: dict) -> str:
    root = root_selector(pattern["id"])
    items = f"{root} [data-motion-item]"
    target = f"{root} [data-motion-target]"
    path = f"{root} [data-motion-path]"
    handle = f"{root} [data-motion-handle]"
    bubble = f"{root} [data-motion-bubble]"
    line = f"{root} [data-motion-line]"
    family = pattern["_family"]
    if family == "pin":
        return js_wrapper(f"""
const root = document.querySelector('{root}');
if (!root) return;
const items = gsap.utils.toArray('{items}');
if (!items.length) return;
const tl = gsap.timeline({{ scrollTrigger: {{ trigger: root, start: 'top top', end: () => '+=' + root.offsetHeight * Math.max(items.length, 2), scrub: 0.85, pin: true }} }});
items.forEach((item, index) => {{
  tl.fromTo(item, {{ autoAlpha: index === 0 ? 1 : 0, y: 56, scale: 0.96 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.55, ease: 'power3.out' }}, index === 0 ? 0 : '<0.2');
  if (index > 0) tl.to(items[index - 1], {{ autoAlpha: 0.25, scale: 0.96, duration: 0.3, ease: 'power2.out' }}, '<');
}});
        """, f"{root}, {items}", ["ScrollTrigger"])
    if family in {"scrub", "image_sequence"}:
        return js_wrapper(f"""
const root = document.querySelector('{root}');
const target = document.querySelector('{target}') || root;
if (!root || !target) return;
gsap.fromTo(target, {{ autoAlpha: 1, yPercent: 10, scale: 1.05 }}, {{
  autoAlpha: 1,
  yPercent: -8,
  scale: 0.96,
  ease: 'none',
  scrollTrigger: {{ trigger: root, start: 'top 85%', end: 'bottom 15%', scrub: true }},
}});
        """, f"{root}, {target}", ["ScrollTrigger"])
    if family == "progress":
        return js_wrapper(f"""
const root = document.querySelector('{root}');
const target = document.querySelector('{target}') || root.querySelector('[data-motion-rail]');
if (!root || !target) return;
gsap.set(target, {{ transformOrigin: 'top center', scaleY: 0 }});
gsap.to(target, {{ scaleY: 1, ease: 'none', scrollTrigger: {{ trigger: root, start: 'top center', end: 'bottom center', scrub: true }} }});
        """, f"{root}, {target}", ["ScrollTrigger"])
    if family == "nav_velocity":
        return js_wrapper(f"""
const nav = document.querySelector('{root}');
if (!nav) return;
ScrollTrigger.create({{
  start: 'top top',
  end: 'bottom bottom',
  onUpdate: (self) => {{
    const velocity = self.getVelocity();
    if (self.direction === 1 && velocity > 180) gsap.to(nav, {{ yPercent: -100, duration: 0.3, ease: 'power2.in', overwrite: true }});
    if (self.direction === -1 || velocity < -180) gsap.to(nav, {{ yPercent: 0, duration: 0.3, ease: 'power2.out', overwrite: true }});
  }},
}});
        """, root, ["ScrollTrigger"])
    if family == "observer":
        return js_wrapper(f"""
const root = document.querySelector('{root}');
if (!root) return;
const sections = gsap.utils.toArray('{items}');
if (sections.length < 2) return;
let index = 0;
gsap.set(sections, {{ autoAlpha: 0, yPercent: 10 }});
gsap.set(sections[0], {{ autoAlpha: 1, yPercent: 0 }});
const gotoSection = (next) => {{
  if (next < 0 || next >= sections.length || next === index) return;
  gsap.timeline().to(sections[index], {{ autoAlpha: 0, yPercent: -8, duration: 0.35, ease: 'power2.out' }}).fromTo(sections[next], {{ autoAlpha: 0, yPercent: 8 }}, {{ autoAlpha: 1, yPercent: 0, duration: 0.45, ease: 'power2.out' }}, '<');
  index = next;
}};
Observer.create({{ target: root, type: 'wheel,touch,pointer', tolerance: 12, preventDefault: true, onUp: () => gotoSection(index + 1), onDown: () => gotoSection(index - 1) }});
        """, f"{root}, {items}", ["Observer"])
    if family == "scrollsmoother":
        return js_wrapper(f"""
if (!document.querySelector('#smooth-wrapper') || !document.querySelector('#smooth-content')) return;
const smoother = ScrollSmoother.create({{ wrapper: '#smooth-wrapper', content: '#smooth-content', smooth: 1.1, effects: true, normalizeScroll: true }});
return () => smoother.kill();
        """, "#smooth-wrapper, #smooth-content", ["ScrollTrigger", "ScrollSmoother"])
    if family == "splittext_lines":
        return js_wrapper(f"""
gsap.utils.toArray('{root}').forEach((block) => {{
  const split = new SplitText(block, {{ type: 'lines', mask: 'lines', autoSplit: true, aria: true }});
  gsap.from(split.lines, {{ yPercent: 110, autoAlpha: 0, duration: 0.85, ease: 'power3.out', stagger: 0.08, scrollTrigger: {{ trigger: block, start: 'top 85%' }}, onComplete: () => split.revert() }});
}});
        """, root, ["SplitText", "ScrollTrigger"])
    if family == "splittext_chars":
        return js_wrapper(f"""
gsap.utils.toArray('{root}').forEach((block) => {{
  const split = new SplitText(block, {{ type: 'chars', aria: true }});
  gsap.from(split.chars, {{ rotationX: -80, yPercent: 110, autoAlpha: 0, transformOrigin: '50% 100%', duration: 0.7, ease: 'power3.out', stagger: {{ each: 0.025, from: 'center' }}, scrollTrigger: {{ trigger: block, start: 'top 85%' }}, onComplete: () => split.revert() }});
}});
        """, root, ["SplitText", "ScrollTrigger"])
    if family == "splittext_random":
        return js_wrapper(f"""
gsap.utils.toArray('{root}').forEach((block) => {{
  const split = new SplitText(block, {{ type: 'words,chars', aria: true }});
  const parts = split.chars.length ? split.chars : split.words;
  gsap.from(parts, {{ yPercent: 100, autoAlpha: 0, duration: 0.55, ease: 'power2.out', stagger: {{ each: 0.03, from: 'random' }}, scrollTrigger: {{ trigger: block, start: 'top 88%' }}, onComplete: () => split.revert() }});
}});
        """, root, ["SplitText", "ScrollTrigger"])
    if family == "scramble":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((node) => {{
  const finalText = node.dataset.scrambleLabel || node.textContent.trim();
  const handler = () => gsap.to(node, {{ duration: 0.6, ease: 'none', scrambleText: {{ text: finalText, chars: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', speed: 0.35, revealDelay: 0.08 }} }});
  node.addEventListener('mouseenter', handler);
  node.addEventListener('focus', handler);
}});
        """, root, ["ScrambleTextPlugin"])
    if family in {"mask", "panel"}:
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((block) => {{
  const target = block.querySelector('[data-motion-target]') || block;
  gsap.fromTo(target, {{ autoAlpha: 0, y: 20, scale: 0.98 }}, {{ autoAlpha: 1, y: 0, scale: 1, duration: 0.35, ease: 'power2.out', stagger: 0.05, scrollTrigger: {{ trigger: block, start: 'top 85%' }} }});
}});
        """, f"{root}, {target}", ["ScrollTrigger"])
    if family == "drawsvg":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((block) => {{
  const path = block.querySelector('[data-motion-path]') || block.querySelector('path');
  if (!path) return;
  gsap.from(path, {{ drawSVG: '0%', duration: 0.8, ease: 'power2.out', scrollTrigger: {{ trigger: block, start: 'top 85%' }} }});
}});
        """, f"{root}, {path}", ["DrawSVGPlugin", "ScrollTrigger"])
    if family == "odometer":
        return js_wrapper(f"""
document.querySelectorAll('{items}').forEach((digit) => {{
  const end = Number(digit.dataset.digit || 0);
  gsap.fromTo(digit, {{ yPercent: 100 }}, {{ yPercent: -100 * end, duration: 0.8, ease: 'power2.out', scrollTrigger: {{ trigger: digit.closest('{root}'), start: 'top 85%' }} }});
}});
        """, items, ["ScrollTrigger"])
    if family == "toggle":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((button) => {{
  const lines = gsap.utils.toArray('[data-motion-line]', button);
  if (lines.length < 2) return;
  button.addEventListener('click', () => {{
    const active = button.classList.toggle('is-active');
    gsap.to(lines[0], {{ y: active ? 6 : 0, rotation: active ? 45 : 0, duration: 0.3, ease: 'power2.out' }});
    gsap.to(lines[1], {{ autoAlpha: active ? 0 : 1, scaleX: active ? 0.6 : 1, duration: 0.2, ease: 'power2.out' }});
    gsap.to(lines[2] || lines[1], {{ y: active ? -6 : 0, rotation: active ? -45 : 0, duration: 0.3, ease: 'power2.out' }});
  }});
}});
        """, f"{root}, {line}")
    if family == "flip_indicator":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((group) => {{
  const indicator = group.querySelector('[data-motion-indicator]');
  const items = gsap.utils.toArray('[data-motion-item]', group);
  if (!indicator || !items.length) return;
  items.forEach((item) => item.addEventListener('click', () => {{
    const state = Flip.getState(indicator);
    item.appendChild(indicator);
    Flip.from(state, {{ duration: 0.45, ease: 'power2.inOut', absolute: true }});
  }}));
}});
        """, root, ["Flip"])
    if family == "accordion":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((item) => {{
  const panel = item.querySelector('[data-motion-panel]');
  if (!panel) return;
  gsap.set(panel, {{ transformOrigin: 'top center', scaleY: 0.92, autoAlpha: 0 }});
  item.addEventListener('click', () => {{
    const open = item.classList.toggle('is-open');
    gsap.to(panel, {{ scaleY: open ? 1 : 0.92, autoAlpha: open ? 1 : 0, duration: 0.3, ease: open ? 'power2.out' : 'power2.in', overwrite: true }});
  }});
}});
        """, root)
    if family == "toast":
        return js_wrapper(f"""
document.querySelectorAll('{items}').forEach((item, index) => {{
  gsap.set(item, {{ y: index * 10, scale: 1 - index * 0.04 }});
  const dismiss = item.querySelector('[data-toast-dismiss]');
  if (!dismiss) return;
  dismiss.addEventListener('click', () => gsap.to(item, {{ x: 64, autoAlpha: 0, duration: 0.25, ease: 'power2.in', onComplete: () => item.remove() }}));
}});
        """, items)
    if family == "tooltip":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((trigger) => {{
  const bubble = trigger.querySelector('[data-motion-bubble]');
  if (!bubble) return;
  const xTo = gsap.quickTo(bubble, 'x', {{ duration: 0.18, ease: 'power3.out' }});
  const yTo = gsap.quickTo(bubble, 'y', {{ duration: 0.18, ease: 'power3.out' }});
  trigger.addEventListener('mouseenter', () => gsap.to(bubble, {{ autoAlpha: 1, scale: 1, duration: 0.18, ease: 'power2.out' }}));
  trigger.addEventListener('mousemove', (event) => {{
    const rect = trigger.getBoundingClientRect();
    xTo(event.clientX - rect.left - rect.width / 2);
    yTo(event.clientY - rect.top - rect.height / 2 - 16);
  }});
  trigger.addEventListener('mouseleave', () => gsap.to(bubble, {{ autoAlpha: 0, scale: 0.96, duration: 0.14, ease: 'power2.out' }}));
}});
        """, f"{root}, {bubble}")
    if family == "form_focus":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((form) => {{
  const fields = gsap.utils.toArray('[data-motion-item]', form);
  fields.forEach((field, index) => {{
    field.addEventListener('focusin', () => gsap.to(fields.slice(index), {{ y: -2, duration: 0.18, ease: 'power2.out', stagger: 0.02 }}));
    field.addEventListener('focusout', () => gsap.to(fields, {{ y: 0, duration: 0.18, ease: 'power2.out', overwrite: true }}));
  }});
}});
        """, root)
    if family == "draggable":
        return js_wrapper(f"""
document.querySelectorAll('{items}').forEach((item, index) => {{
  gsap.set(item, {{ y: index * 8, rotation: (index - 1) * 2 }});
  Draggable.create(item, {{ type: 'x,y', inertia: true, onPress() {{ gsap.to(item, {{ scale: 1.02, duration: 0.15, ease: 'power2.out' }}) }}, onRelease() {{ gsap.to(item, {{ scale: 1, duration: 0.2, ease: 'power2.out' }}) }} }});
}});
        """, items, ["Draggable"])
    if family == "loop":
        return js_wrapper(f"""
const items = gsap.utils.toArray('{items}');
if (!items.length) return;
const width = items.reduce((total, item) => total + item.offsetWidth, 0);
gsap.to(items, {{ x: `-=${{width}}`, duration: 18, ease: 'none', repeat: -1, modifiers: {{ x: (value) => `${{gsap.utils.wrap(-width, 0, parseFloat(value))}}px` }} }});
        """, items)
    if family == "before_after":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((block) => {{
  const handle = block.querySelector('{handle}');
  const target = block.querySelector('[data-motion-target]');
  if (!handle || !target) return;
  const update = () => {{
    const progress = gsap.utils.clamp(0, 1, (handle.offsetLeft || 0) / block.getBoundingClientRect().width);
    gsap.set(target, {{ transformOrigin: 'left center', scaleX: progress }});
  }};
  Draggable.create(handle, {{ type: 'x', bounds: block, inertia: true, onDrag: update, onThrowUpdate: update }});
}});
        """, f"{root}, {handle}, {target}", ["Draggable"])
    if family == "cursor_preview":
        return js_wrapper(f"""
const preview = document.querySelector('{target}');
if (!preview) return;
const xTo = gsap.quickTo(preview, 'x', {{ duration: 0.2, ease: 'power3.out' }});
const yTo = gsap.quickTo(preview, 'y', {{ duration: 0.2, ease: 'power3.out' }});
document.querySelectorAll('{items}').forEach((item) => {{
  item.addEventListener('mouseenter', () => gsap.to(preview, {{ autoAlpha: 1, scale: 1, duration: 0.18, ease: 'power2.out' }}));
  item.addEventListener('mousemove', (event) => {{ xTo(event.clientX + 18); yTo(event.clientY + 18); }});
  item.addEventListener('mouseleave', () => gsap.to(preview, {{ autoAlpha: 0, scale: 0.96, duration: 0.16, ease: 'power2.out' }}));
}});
        """, f"{items}, {target}")
    if family == "video_scrub":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((card) => {{
  const video = card.querySelector('video');
  if (!video) return;
  const state = {{ progress: 0 }};
  const update = () => video.duration && (video.currentTime = state.progress * video.duration);
  card.addEventListener('mouseenter', () => gsap.to(state, {{ progress: 1, duration: 0.9, ease: 'power2.out', onUpdate: update }}));
  card.addEventListener('mouseleave', () => gsap.to(state, {{ progress: 0, duration: 0.45, ease: 'power2.out', onUpdate: update }}));
}});
        """, root)
    if family == "shared_expand":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((gallery) => {{
  const expanded = gallery.querySelector('[data-motion-expanded]');
  const items = gsap.utils.toArray('[data-motion-item]', gallery);
  if (!expanded || !items.length) return;
  items.forEach((item) => item.addEventListener('click', () => {{
    const state = Flip.getState([item, expanded]);
    expanded.appendChild(item);
    expanded.classList.add('is-open');
    Flip.from(state, {{ duration: 0.55, ease: 'power2.inOut', absolute: true }});
  }}));
}});
        """, root, ["Flip"])
    if family == "reorder":
        return js_wrapper(f"""
document.querySelectorAll('{items}').forEach((item) => {{
  Draggable.create(item, {{ type: 'x,y', onRelease() {{ const state = Flip.getState('{items}'); item.parentNode.appendChild(item); Flip.from(state, {{ duration: 0.45, ease: 'power2.inOut', absolute: true }}); gsap.to(item, {{ x: 0, y: 0, duration: 0.2, ease: 'power2.out' }}); }} }});
}});
        """, items, ["Draggable", "Flip"])
    if family == "stack":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((stack) => {{
  const items = gsap.utils.toArray('[data-motion-item]', stack);
  const layout = () => items.forEach((item, index) => gsap.to(item, {{ y: index * 12, scale: 1 - index * 0.04, duration: 0.25, ease: 'power2.out' }}));
  layout();
  stack.querySelector('[data-motion-next]')?.addEventListener('click', () => {{ items.push(items.shift()); layout(); }});
}});
        """, root)
    if family == "motionpath":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((block) => {{
  const target = block.querySelector('[data-motion-target]');
  const path = block.querySelector('[data-motion-path]');
  if (!target || !path) return;
  gsap.to(target, {{ duration: 8, repeat: -1, ease: 'none', motionPath: {{ path, align: path, autoRotate: false, alignOrigin: [0.5, 0.5] }} }});
}});
        """, f"{root}, {path}, {target}", ["MotionPathPlugin"])
    if family == "morph":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((block) => {{
  const shapes = gsap.utils.toArray('[data-motion-shape]', block);
  if (shapes.length < 2) return;
  const tl = gsap.timeline({{ repeat: -1, repeatDelay: 0.6 }});
  for (let index = 1; index < shapes.length; index += 1) tl.to(shapes[0], {{ morphSVG: shapes[index], duration: 0.8, ease: 'power2.inOut' }});
}});
        """, root, ["MorphSVGPlugin"])
    if family == "burst":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((button) => {{
  const items = gsap.utils.toArray('[data-motion-item]', button);
  button.addEventListener('click', () => items.forEach((item, index) => {{
    const angle = (Math.PI * 2 * index) / Math.max(items.length, 1);
    gsap.fromTo(item, {{ x: 0, y: 0, scale: 0.4, autoAlpha: 1 }}, {{ x: Math.cos(angle) * 32, y: Math.sin(angle) * 32, scale: 1, autoAlpha: 0, duration: 0.45, ease: 'power2.out' }});
  }}));
}});
        """, root)
    if family == "loader":
        return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((loader) => {{
  const dots = gsap.utils.toArray('[data-motion-item]', loader);
  gsap.to(loader, {{ rotation: 360, transformOrigin: '50% 50%', duration: 1.4, ease: 'none', repeat: -1 }});
  dots.forEach((dot, index) => gsap.to(dot, {{ scale: 0.6, yoyo: true, repeat: -1, duration: 0.7, delay: index * 0.12, ease: 'power2.inOut' }}));
}});
        """, root)
    return js_wrapper(f"""
document.querySelectorAll('{root}').forEach((node) => {{
  gsap.fromTo(node, {{ autoAlpha: 0, y: 24 }}, {{ autoAlpha: 1, y: 0, duration: 0.45, ease: 'power2.out', scrollTrigger: {{ trigger: node, start: 'top 85%' }} }});
}});
    """, root, ["ScrollTrigger"])


def spec_document(pattern: dict) -> OrderedDict:
    root = root_selector(pattern["id"])
    target_type = "group" if pattern["_family"] in {"pin", "observer", "splittext_lines", "splittext_chars", "splittext_random", "draggable", "loop", "reorder", "stack", "loader"} else "element"
    trigger_type = pattern["triggers"][0].replace("page-load", "load").replace("scroll-enter", "scroll")
    data = OrderedDict(
        [
            ("version", "1"),
            ("type", pattern["type"]),
            ("id", pattern["id"]),
            ("target", OrderedDict([("selector", root), ("type", target_type)])),
            ("timing", OrderedDict([("duration", "base" if pattern["category"] != "ambient" else "slow"), ("easing", "transition" if pattern["category"] == "transition" else "entrance")])),
            ("trigger", OrderedDict([("type", trigger_type)])),
            ("a11y", OrderedDict([("reduced_motion", "instant-final")])),
            ("plugins", [key for key, url in URLS.items() if url in pattern["sources"] and key != "codrops"]),
            ("config", OrderedDict([("root", root), ("items", f"{root} [data-motion-item]"), ("target", f"{root} [data-motion-target]"), ("path", f"{root} [data-motion-path]")])),
        ]
    )
    if pattern["category"] == "scroll":
        data["trigger"]["scroll_start"] = "top 85%"
    if pattern["type"] == "procedural":
        data["behavior"] = pattern["description"]
    return data


def index_markdown(pattern: dict) -> str:
    return "\n".join(
        [
            f"# {pattern['name']}",
            "",
            f"**Framework:** {pattern['framework']}",
            f"**Category:** {pattern['category']}",
            f"**2026 Relevance:** {'Still active in March 2026 because it maps cleanly to current GSAP patterns and interface expectations.' if pattern['status'] != 'emerging' else 'Current in March 2026 because it is appearing in premium GSAP-heavy builds without becoming a default trope yet.'}",
            "",
            "## Description",
            "",
            textwrap.fill(pattern["description"], width=88),
            "",
            textwrap.fill(pattern["_best_for"], width=88),
            "",
            "## Do's",
            "",
            "- Keep reduced-motion behavior explicit and leave the static end state readable immediately.",
            "- Scope selectors to the local section or component rather than targeting the whole page.",
            "- Prefer transform and autoAlpha changes over layout-triggering properties.",
            "",
            "## Don'ts",
            "",
            "- Do not stack the same effect on every similar surface in the viewport.",
            "- Do not leave decorative motion running without checking touch and reduced-motion behavior.",
            "- Do not convert a state-change pattern into ambient motion just because the effect looks good.",
            "",
            "## Best Practices",
            "",
            textwrap.fill(pattern["_feel"], width=88),
            "",
            textwrap.fill(pattern["_avoid"], width=88),
            "",
            "Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.",
            "",
        ]
    )


def write_new_patterns(patterns: list[dict]) -> None:
    for pattern in patterns:
        folder = LIB_DIR / pattern["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.md").write_text(index_markdown(pattern), encoding="utf-8")
        (folder / "spec.yaml").write_text(yaml.safe_dump(plain(spec_document(pattern)), sort_keys=False, allow_unicode=False), encoding="utf-8")
        (folder / "snippet.js").write_text(snippet_for(pattern), encoding="utf-8")


def normalize_lenis_snippet() -> None:
    snippet = """const mm = gsap.matchMedia();
mm.add(\"(prefers-reduced-motion: no-preference)\", () => {
  const lenis = new Lenis({
    duration: 1.2,
    easing: (value) => Math.min(1, 1.001 - Math.pow(2, -10 * value)),
    orientation: \"vertical\",
    smoothWheel: true,
  });

  lenis.on(\"scroll\", ScrollTrigger.update);
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);

  return () => {
    lenis.destroy();
  };
});
mm.add(\"(prefers-reduced-motion: reduce)\", () => {
  ScrollTrigger.update();
});
    """
    (LIB_DIR / "lenis-smooth-scroll" / "snippet.js").write_text(snippet, encoding="utf-8")


def normalize_legacy_snippets() -> None:
    snippets = {
        "3d-tilt-parallax-cursor": """const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll(".tilt-card, [data-tilt-card]").forEach((card) => {
    const xTo = gsap.quickTo(card, "rotationY", { duration: 0.2, ease: "power3.out" });
    const yTo = gsap.quickTo(card, "rotationX", { duration: 0.2, ease: "power3.out" });
    card.addEventListener("mouseenter", () => {
      gsap.to(card, { scale: 1.03, duration: 0.2, ease: "power2.out" });
    });
    card.addEventListener("mousemove", (event) => {
      const rect = card.getBoundingClientRect();
      const offsetX = (event.clientX - rect.left - rect.width / 2) / rect.width;
      const offsetY = (event.clientY - rect.top - rect.height / 2) / rect.height;
      xTo(offsetX * 18);
      yTo(offsetY * -18);
    });
    card.addEventListener("mouseleave", () => {
      xTo(0);
      yTo(0);
      gsap.to(card, { scale: 1, duration: 0.25, ease: "power2.out" });
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".tilt-card, [data-tilt-card]", { clearProps: "all" });
});
""",
        "ambient-floating-particles": """const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const canvas = document.getElementById("particle-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const particles = Array.from({ length: 40 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    r: 1 + Math.random() * 2,
    o: 0.04 + Math.random() * 0.12,
  }));

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  resize();
  window.addEventListener("resize", resize, { passive: true });

  particles.forEach((particle) => {
    gsap.to(particle, {
      x: () => Math.random() * window.innerWidth,
      y: () => Math.random() * window.innerHeight,
      o: () => 0.04 + Math.random() * 0.12,
      duration: () => 18 + Math.random() * 20,
      ease: "none",
      repeat: -1,
      yoyo: true,
    });
  });

  gsap.ticker.add(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((particle) => {
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(160,170,220,${particle.o})`;
      ctx.fill();
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {});
""",
        "bento-grid-motion": """gsap.registerPlugin(Flip);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const grid = document.querySelector(".bento-grid");
  if (!grid) return;
  const cards = gsap.utils.toArray(".bento-grid .bento-card");
  cards.forEach((card) => {
    card.addEventListener("click", () => {
      const state = Flip.getState(cards);
      const expanded = card.classList.contains("bento-card--expanded");
      cards.forEach((item) => item.classList.remove("bento-card--expanded"));
      if (!expanded) card.classList.add("bento-card--expanded");
      Flip.from(state, { duration: 0.45, ease: "power2.inOut", absolute: true, nested: true });
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".bento-grid .bento-card", { clearProps: "all" });
});
""",
        "gesture-swipe-animations": """const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-swipe-card], .card").forEach((card) => {
    let startX = 0;
    card.addEventListener("pointerdown", (event) => {
      startX = event.clientX;
      card.setPointerCapture?.(event.pointerId);
    });
    card.addEventListener("pointermove", (event) => {
      if (!startX) return;
      const deltaX = event.clientX - startX;
      gsap.to(card, { x: deltaX, rotation: deltaX * 0.03, duration: 0, overwrite: true });
    });
    const reset = () => {
      startX = 0;
      gsap.to(card, { x: 0, rotation: 0, duration: 0.25, ease: "power2.out" });
    };
    card.addEventListener("pointerup", reset);
    card.addEventListener("pointercancel", reset);
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-swipe-card], .card", { clearProps: "all" });
});
""",
        "number-counter-easing": """gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-counter]").forEach((element) => {
    const value = Number(element.getAttribute("data-counter") || 0);
    const state = { value: Number(element.getAttribute("data-start") || 0) };
    const render = () => {
      element.textContent = Math.round(state.value).toLocaleString();
    };
    render();
    gsap.to(state, {
      value,
      duration: Number(element.getAttribute("data-duration") || 1.6),
      ease: element.getAttribute("data-easing") || "power2.out",
      scrollTrigger: { trigger: element, start: "top 85%", once: true },
      onUpdate: render,
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {});
""",
        "ripple-wave-click": """const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-ripple], button, a, .ripple-trigger");
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const ripple = document.createElement("span");
    ripple.style.position = "absolute";
    ripple.style.left = `${event.clientX - rect.left}px`;
    ripple.style.top = `${event.clientY - rect.top}px`;
    ripple.style.width = "12px";
    ripple.style.height = "12px";
    ripple.style.borderRadius = "999px";
    ripple.style.background = "currentColor";
    ripple.style.opacity = "0.22";
    ripple.style.pointerEvents = "none";
    ripple.style.transform = "translate(-50%, -50%) scale(0)";
    if (getComputedStyle(target).position === "static") target.style.position = "relative";
    if (getComputedStyle(target).overflow !== "hidden") target.style.overflow = "hidden";
    target.appendChild(ripple);
    gsap.to(ripple, {
      scale: 18,
      autoAlpha: 0,
      duration: 0.55,
      ease: "power2.out",
      onComplete: () => ripple.remove(),
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {});
""",
        "staggered-word-reveal": """gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-word-reveal]").forEach((element) => {
    const words = element.textContent.trim().split(/\\s+/);
    element.innerHTML = words.map((word) => `<span class=\"word-reveal\" style=\"display:inline-block;margin-right:0.25em\">${word}</span>`).join("");
    gsap.from(element.querySelectorAll(".word-reveal"), {
      autoAlpha: 0,
      y: 12,
      duration: 0.7,
      ease: "power2.out",
      stagger: 0.09,
      scrollTrigger: { trigger: element, start: "top 85%", once: true },
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-word-reveal]", { clearProps: "all" });
});
""",
        "text-scramble-decode": """gsap.registerPlugin(ScrambleTextPlugin);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-scramble-text]").forEach((element) => {
    const finalText = element.dataset.scrambleText || element.textContent.trim();
    gsap.to(element, {
      duration: 1.1,
      ease: "none",
      scrambleText: {
        text: finalText,
        chars: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*",
        speed: 0.35,
        revealDelay: 0.1,
      },
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  document.querySelectorAll("[data-scramble-text]").forEach((element) => {
    element.textContent = element.dataset.scrambleText || element.textContent.trim();
  });
});
""",
    }
    for folder_name, snippet in snippets.items():
        (LIB_DIR / folder_name / "snippet.js").write_text(snippet, encoding="utf-8")


def ordered_catalog(existing: list[dict], new: list[dict]) -> list[OrderedDict]:
    result = []
    for entry in existing + new:
        result.append(OrderedDict((key, value) for key, value in entry.items() if not key.startswith("_")))
    return result


def write_catalog(patterns: list[OrderedDict]) -> None:
    header = "\n".join(
        [
            'version: "1"',
            "# Motion Library Catalog — Structural metadata for all patterns",
            "# For trend narrative context (what, when, how it should feel), see trends-overview.md",
            "# Each pattern lives in its own folder: <folder>/index.md, <folder>/spec.yaml, <folder>/snippet.css|js",
            "",
        ]
    )
    body = yaml.safe_dump({"patterns": plain(patterns)}, sort_keys=False, allow_unicode=False)
    CATALOG_PATH.write_text(header + body, encoding="utf-8")


def overview_markdown(patterns: list[dict]) -> str:
    grouped = defaultdict(list)
    for pattern in patterns:
        grouped[pattern["category"]].append(pattern)
    lines = [
        "# Motion Library — Trends Overview",
        f"> Quick-load reference for pattern selection. Read this instead of opening all {len(patterns)} pattern folders.",
        "> Machine-readable scoring lives in catalog.yaml. Full prose and implementation details live in pattern folders.",
        f"> Last updated: {TODAY_DAY}",
        "",
        "---",
        "",
    ]
    for category in CATEGORY_ORDER:
        if category not in grouped:
            continue
        lines.append(f"## {kebab_to_title(category)}")
        lines.append("")
        for pattern in sorted(grouped[category], key=lambda item: (-int(item['trend_score']), item['id'])):
            lines.append(f"### {pattern['name']}  [{pattern['category']} | {pattern['framework']} | {pattern['status']} {pattern['trend_score']}/10]")
            lines.append(f"- What: {pattern['description']}")
            lines.append(f"- Best for: {pattern['_best_for']}")
            lines.append(f"- Feel: {pattern['_feel']}")
            lines.append(f"- Avoid: {pattern['_avoid']}")
            lines.append("")
    lines.extend(["---", "", "## Quick Table", "", "| Pattern | Category | Framework | Score | Status | Best for |", "|---|---|---|---:|---|---|"])
    for pattern in sorted(patterns, key=lambda item: (CATEGORY_ORDER.index(item["category"]) if item["category"] in CATEGORY_ORDER else 99, -int(item["trend_score"]), item["id"])):
        lines.append(f"| `{pattern['id']}` | {pattern['category']} | {pattern['framework']} | {pattern['trend_score']} | {pattern['status']} | {pattern['_best_for'].rstrip('.')} |")
    lines.append("")
    return "\n".join(lines)


def write_scores(catalog_patterns: list[dict], context_map: dict[str, list[str]]) -> None:
    buckets = defaultdict(lambda: defaultdict(list))
    for entry in catalog_patterns:
        if entry["status"] == "declining":
            continue
        score = int(entry["trend_score"] or 0)
        for component in entry["components"]:
            buckets[component]["any"].append((score, entry["id"]))
            for context in context_map.get(entry["id"], []):
                buckets[component][context].append((score, entry["id"]))

    lines = [
        "# element_type -> site_context -> ranked pattern IDs",
        "# AUTO-GENERATED by /motion-refresh or .claude/scripts/generate_motion_library.py — do not edit manually",
        "# Regenerate with: python .claude/scripts/generate_motion_library.py",
        f"# Last updated: {TODAY_DAY}",
        "",
        '# Usage: look up element type, then site_context (fall back to "any")',
        "# First pattern in list = top recommendation for that element + context",
        "",
    ]
    for component in sorted(buckets):
        lines.append(f"{component}:")
        for context in [*SITE_CONTEXTS, "any"]:
            if context not in buckets[component]:
                continue
            ordered = [pattern_id for _, pattern_id in sorted(buckets[component][context], key=lambda item: (-item[0], item[1]))]
            lines.append(f"  {context}: [{', '.join(ordered)}]")
        lines.append("")
    lines.append("site_contexts:")
    for context, payload in SITE_CONTEXT_OVERRIDES.items():
        parts = [f"personality: {payload['personality']}"]
        if payload.get("prefer"):
            parts.append(f"prefer: [{', '.join(payload['prefer'])}]")
        if payload.get("avoid"):
            parts.append(f"avoid: [{', '.join(payload['avoid'])}]")
        lines.append(f"  {context}: {{{', '.join(parts)}}}")
    lines.append("")
    SCORES_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    new = derive_new_patterns()
    new_ids = {entry["id"] for entry in new}
    existing = [entry for entry in normalize_existing_patterns() if entry["id"] not in new_ids]
    write_new_patterns(new)
    normalize_lenis_snippet()
    normalize_legacy_snippets()

    catalog_patterns = ordered_catalog(existing, new)
    write_catalog(catalog_patterns)

    all_for_overview = existing + new
    OVERVIEW_PATH.write_text(overview_markdown(all_for_overview), encoding="utf-8")

    context_map = {entry["id"]: entry["_contexts"] for entry in all_for_overview}
    write_scores(catalog_patterns, context_map)
    print(f"Generated {len(new)} new patterns; catalog now contains {len(catalog_patterns)} entries.")


if __name__ == "__main__":
    main()
