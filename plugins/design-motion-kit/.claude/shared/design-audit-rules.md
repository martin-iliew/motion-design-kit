# Design Audit Rules

Use this rubric for `design-audit` and the audit pass inside `design-upgrade`.

## Part A: Surface Decision Table

- weak hero -> `grid-led-hero`
- weak proof near top -> `sticky-proof-strip`
- weak product explanation -> `product-ui-showcase`
- weak features section -> `modular-feature-grid`
- weak integrations proof -> `integration-logo-ecosystem`
- weak pricing clarity -> `comparison-pricing-matrix`
- weak testimonials -> `outcome-testimonial-wall`
- weak objections handling -> `objection-handling-faq`
- weak closing CTA -> `risk-reversal-cta-band`
- weak trust or compliance -> `security-compliance-block`
- weak case-study proof -> `customer-story-metrics`

## Part B: Severity

- `CRITICAL`: confusing offer, broken hierarchy, absent CTA path, missing trust on trust-sensitive pages, raw-value-heavy implementation
- `WARNING`: weak proof density, generic sections, poor feature grouping, inconsistent design system usage
- `INFO`: additional polish, stronger metric framing, better proof labeling

## Part C: Audit Dimensions

- `MESSAGE`: what it is, who it is for, and why it matters
- `HIERARCHY`: headline flow, grouping, and scanability
- `PROOF`: logos, metrics, customer evidence, and trust placement
- `CONVERSION`: clarity and repetition of the CTA path
- `TOKENS`: whether implementation uses the design system instead of raw values

## Part D: Hard No List

- brutalism by default
- anti-grid composition
- vague headlines with no audience or outcome
- screenshots without explanation
- testimonial sections with no customer identity or outcome
- pricing cards that hide key differences
- raw spacing, color, or radius values when token aliases exist
