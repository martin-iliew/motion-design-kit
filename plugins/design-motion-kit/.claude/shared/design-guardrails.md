# Design Guardrails

These rules are mandatory in every mode.

## Conversion

- above the fold must communicate product, audience, and outcome
- the primary CTA must be visible, specific, and repeated later when needed
- proof must appear within the first two major scrolls
- pricing, objections, or trust gaps cannot be replaced by decorative filler

## Composition

- use real grid discipline
- keep section widths, spacing, and text measures production-safe
- allow asymmetry only when it still reads as intentional and orderly
- one strong design move per section is better than several weak ones

## Design-System Discipline

- DTCG is the canonical token source
- Tailwind v4 theme output is derived, not hand-authored
- do not introduce raw spacing, color, radius, shadow, typography, or timing values in generated code
- map implementation decisions through `brief/token-aliases.json`

## Motion Readiness

- only emit motion hints for elements that the selected design actually creates
- motion hints must describe allowed families and intensity, not implementation code
- structure must remain legible and useful without motion

## Implementation Hygiene

- reuse existing components when reasonable
- prefer clear component boundaries over wrapper-heavy markup
- preserve semantic heading order and mobile readability
