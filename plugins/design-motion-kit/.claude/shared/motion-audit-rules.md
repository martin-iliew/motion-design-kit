# Motion Audit Rules

Use this rubric for `motion-audit` and the audit pass inside `motion-upgrade`.

## Part A: Element Decision Table

- fixed nav without scroll reactivity -> smart hide/show
- static hero heading -> hero entrance timeline
- feature or pricing cards without entrance -> stagger scroll reveal
- plain section headings -> section reveal
- interactive cards without response -> spring hover
- stat numbers -> number counter
- pinned walkthrough -> pinned scrub
- filterable grid -> FLIP layout
- desktop CTA or button -> tactile micro-interaction

## Part B: Severity

- `CRITICAL`: missing reduced-motion, layout-triggering properties, conflicting ownership, missing cleanup
- `WARNING`: stale motion vocabulary, weak interaction coverage, inconsistent timing system
- `INFO`: optional polish or richer sequencing

## Part C: Hard Rules

- use `autoAlpha` for GSAP entrances
- use `gsap.matchMedia()` for reduced-motion and desktop gating
- remove CSS transitions from GSAP-owned properties
- never animate absent elements
- never violate `brief/motion-hints.yaml` when it exists

## Part D: Token Quick Reference

- duration tokens: `micro`, `fast`, `base`, `slow`, `epic`
- easing tokens: `entrance`, `impact`, `transition`, `exit`, `spring`, `elastic`, `scrub`
- stagger tokens: `tight`, `medium`, `loose`
