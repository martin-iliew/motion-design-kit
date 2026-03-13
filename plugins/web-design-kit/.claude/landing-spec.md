# Landing Spec

A **Landing Spec** is a stack-agnostic YAML document that describes a single landing-page pattern or section. It captures design intent in a way that HTML/CSS, Tailwind, React, Vue, or design-system implementations can all consume.

Use Landing Spec when:

- `web-build` needs a neutral contract before writing code
- `web-discover` is generating a new pattern folder
- maintainers want a clean pattern description without binding it to one framework

## Required fields

```yaml
version: "1"
id: grid-led-hero
intent: clarify the offer fast with proof and product context
surfaces:
  - hero
  - cta
  - media
structure:
  desktop: 12-col split with copy on the left and product media on the right
  mobile: single column with proof directly below the CTA
proof:
  above_fold: true
  type: logos | metrics | badge
cta:
  primary: start-free | book-demo | contact-sales
  secondary: watch-demo | see-pricing | explore-product
responsive:
  stack_at: 960px
accessibility:
  heading_order: h1-first
  media_alt_required: true
```

## Principles

- Describe what the section should accomplish before describing how it looks.
- Prefer clarity, proof, and scannability over novelty.
- Keep the first screen answerable: what it is, who it is for, why it matters, and what to do next.
- Use this spec to preserve intent across code rewrites or framework translation.
