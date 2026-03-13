from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT / "design-library"
CATALOG_PATH = LIB_DIR / "catalog.yaml"
SCORES_PATH = LIB_DIR / "scores.yaml"
BASELINES_PATH = LIB_DIR / "site-baselines.yaml"
WATCHLIST_PATH = LIB_DIR / "trend-watchlist.yaml"


SURFACE_PRIORITIES = {
    "hero": {
        "saas": ["grid-led-hero", "product-ui-showcase"],
        "ai": ["grid-led-hero", "product-ui-showcase", "customer-story-metrics"],
        "enterprise": ["grid-led-hero", "security-compliance-block"],
        "developer-tools": ["grid-led-hero", "product-ui-showcase", "integration-logo-ecosystem"],
        "any": ["grid-led-hero", "product-ui-showcase"],
    },
    "proof": {
        "saas": ["sticky-proof-strip", "customer-story-metrics", "outcome-testimonial-wall"],
        "ai": ["sticky-proof-strip", "customer-story-metrics", "security-compliance-block"],
        "enterprise": ["security-compliance-block", "sticky-proof-strip", "customer-story-metrics"],
        "developer-tools": ["integration-logo-ecosystem", "sticky-proof-strip", "customer-story-metrics"],
        "ecommerce": ["sticky-proof-strip", "outcome-testimonial-wall"],
        "any": ["sticky-proof-strip", "customer-story-metrics", "outcome-testimonial-wall"],
    },
    "metrics": {
        "saas": ["customer-story-metrics", "sticky-proof-strip"],
        "ai": ["customer-story-metrics", "sticky-proof-strip"],
        "enterprise": ["customer-story-metrics", "security-compliance-block"],
        "any": ["customer-story-metrics", "sticky-proof-strip"],
    },
    "product": {
        "saas": ["product-ui-showcase", "modular-feature-grid"],
        "ai": ["product-ui-showcase", "modular-feature-grid"],
        "developer-tools": ["product-ui-showcase", "integration-logo-ecosystem"],
        "any": ["product-ui-showcase", "modular-feature-grid"],
    },
    "features": {
        "saas": ["modular-feature-grid", "product-ui-showcase"],
        "ai": ["modular-feature-grid", "product-ui-showcase"],
        "developer-tools": ["modular-feature-grid", "product-ui-showcase"],
        "ecommerce": ["modular-feature-grid"],
        "any": ["modular-feature-grid", "product-ui-showcase"],
    },
    "integrations": {
        "saas": ["integration-logo-ecosystem"],
        "ai": ["integration-logo-ecosystem"],
        "enterprise": ["integration-logo-ecosystem", "security-compliance-block"],
        "developer-tools": ["integration-logo-ecosystem"],
        "any": ["integration-logo-ecosystem"],
    },
    "pricing": {
        "saas": ["comparison-pricing-matrix", "risk-reversal-cta-band"],
        "ai": ["comparison-pricing-matrix", "risk-reversal-cta-band"],
        "enterprise": ["comparison-pricing-matrix", "security-compliance-block"],
        "developer-tools": ["comparison-pricing-matrix"],
        "any": ["comparison-pricing-matrix", "risk-reversal-cta-band"],
    },
    "testimonial": {
        "saas": ["customer-story-metrics", "outcome-testimonial-wall"],
        "ai": ["customer-story-metrics", "outcome-testimonial-wall"],
        "enterprise": ["customer-story-metrics", "outcome-testimonial-wall"],
        "ecommerce": ["outcome-testimonial-wall"],
        "any": ["customer-story-metrics", "outcome-testimonial-wall"],
    },
    "security": {
        "enterprise": ["security-compliance-block"],
        "saas": ["security-compliance-block", "sticky-proof-strip"],
        "ai": ["security-compliance-block"],
        "developer-tools": ["security-compliance-block"],
        "any": ["security-compliance-block"],
    },
    "faq": {
        "saas": ["objection-handling-faq"],
        "ai": ["objection-handling-faq"],
        "enterprise": ["objection-handling-faq", "security-compliance-block"],
        "ecommerce": ["objection-handling-faq"],
        "any": ["objection-handling-faq"],
    },
    "cta": {
        "saas": ["risk-reversal-cta-band", "sticky-proof-strip"],
        "ai": ["risk-reversal-cta-band", "sticky-proof-strip"],
        "enterprise": ["risk-reversal-cta-band", "security-compliance-block"],
        "ecommerce": ["risk-reversal-cta-band"],
        "any": ["risk-reversal-cta-band", "sticky-proof-strip"],
    },
}

SITE_BASELINES = {
    "saas": {
        "required_sections": ["hero", "proof", "product", "features", "pricing", "faq", "cta"],
        "preferred_proof": ["logos", "metrics", "customer-story"],
        "tone": "clear, product-led, concise",
        "avoid": ["brutalism", "anti-grid", "novelty-collage"],
    },
    "ai": {
        "required_sections": ["hero", "proof", "product", "features", "faq", "cta"],
        "preferred_proof": ["metrics", "logos", "workflow-example"],
        "tone": "clear, confident, outcome-first",
        "avoid": ["speculative-art-direction", "vague-future-copy", "novelty-collage"],
    },
    "enterprise": {
        "required_sections": ["hero", "proof", "security", "product", "pricing", "faq", "cta"],
        "preferred_proof": ["logos", "compliance", "customer-story"],
        "tone": "credible, calm, procurement-safe",
        "avoid": ["brutalism", "anti-grid", "playful-chaos"],
    },
    "developer-tools": {
        "required_sections": ["hero", "proof", "product", "features", "integrations", "pricing", "cta"],
        "preferred_proof": ["logos", "ecosystem", "usage-metrics"],
        "tone": "technical, direct, product-led",
        "avoid": ["oversized-marketing-fluff", "vague-brand-copy", "novelty-collage"],
    },
    "ecommerce": {
        "required_sections": ["hero", "proof", "product", "testimonial", "faq", "cta"],
        "preferred_proof": ["logos", "outcomes", "trust-badges"],
        "tone": "clear, persuasive, visually anchored",
        "avoid": ["editorial-chaos", "low-contrast-type", "novelty-collage"],
    },
    "any": {
        "required_sections": ["hero", "proof", "cta"],
        "preferred_proof": ["logos", "metrics"],
        "tone": "clear, direct",
        "avoid": ["brutalism", "anti-grid", "novelty-collage"],
    },
}

WATCH_REASONS = {
    "customer-story-metrics": "quantified customer proof blocks are increasingly used to bridge product claims and buyer trust.",
    "product-ui-showcase": "product-led homepages keep leaning on clear UI framing instead of abstract illustration-only heroes.",
    "modular-feature-grid": "easy to over-style; keep the layout disciplined and information-carrying.",
    "outcome-testimonial-wall": "only works when customer identity and outcomes are specific.",
}


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_yaml(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=False)


def compile_scores() -> dict:
    return SURFACE_PRIORITIES


def compile_baselines() -> dict:
    return SITE_BASELINES


def compile_watchlist(catalog: dict) -> dict:
    patterns = catalog["patterns"]
    by_id = {pattern["id"]: pattern for pattern in patterns}
    rising = [
        {"id": pattern_id, "reason": WATCH_REASONS[pattern_id]}
        for pattern_id in ("customer-story-metrics", "product-ui-showcase")
        if pattern_id in by_id
    ]
    stable_order = [
        "grid-led-hero",
        "sticky-proof-strip",
        "modular-feature-grid",
        "comparison-pricing-matrix",
        "objection-handling-faq",
        "risk-reversal-cta-band",
        "security-compliance-block",
    ]
    stable = [{"id": pattern_id} for pattern_id in stable_order if pattern_id in by_id]
    watch = [
        {"id": pattern_id, "reason": WATCH_REASONS[pattern_id]}
        for pattern_id in ("modular-feature-grid", "outcome-testimonial-wall")
        if pattern_id in by_id
    ]
    return {"rising": rising, "stable": stable, "watch": watch}


def main() -> None:
    catalog = load_catalog()
    write_yaml(SCORES_PATH, compile_scores())
    write_yaml(BASELINES_PATH, compile_baselines())
    write_yaml(WATCHLIST_PATH, compile_watchlist(catalog))


if __name__ == "__main__":
    main()
