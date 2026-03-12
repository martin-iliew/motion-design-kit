# Motion-Dev Transcript: SOLL Wellness Landing Page

## Task
Animate a wellness landing page with calm, nature-rooted motion that "feels like breathing, not bouncing." Add scroll-triggered reveals for each section and a subtle parallax on the hero.

## Phase 1 — Element Audit

### Site Context Detection
- **Detected:** marketing (single hero CTA, brand copy, minimal nav, nature-rooted wellness brand)
- **Personality override:** `subtle` instead of default `energetic` for marketing — the user explicitly requested calm motion ("breathing, not bouncing")
- **Personality tokens:** Duration bias `base`-`slow` (0.6-1.0s), easing `entrance` (power2.out), stagger `loose` (0.13s)

### Reference Files Loaded
1. `.claude/motion-library/scores.yaml` — element-to-pattern index
2. `.claude/motion-library/trends-overview.md` — pattern context ("how it should feel", "when NOT to use")
3. `references/gsap-patterns.md` — 17 GSAP production templates
4. `references/css-patterns.md` — 4 CSS-only patterns
5. `shared/audit-rules.md` — Parts A, C, D, E (element decision table, hard rules, easing table, token reference)

### Animation Plan
```
1.  Nav             → smart hide/show (Pattern #2)
2.  Hero badge      → hero entrance timeline (Pattern #1)
3.  Hero h1         → SplitText word-level mask reveal (Pattern #9) — slow, gentle
4.  Hero body       → hero entrance timeline (Pattern #1)
5.  Hero CTAs       → hero entrance timeline (Pattern #1) + magnetic pull (Pattern #3, desktop)
6.  Hero metrics    → hero entrance timeline (Pattern #1) — fade only
7.  Hero image      → hero timeline (Pattern #1) + parallax scrub (Pattern #5, desktop)
8.  Rituals label/heading → section reveal (Pattern #6)
9.  Ritual cards    → stagger scroll reveal (Pattern #4) + spring hover (Pattern #7, restrained)
10. Products label/heading → section reveal (Pattern #6)
11. Product cards   → stagger scroll reveal (Pattern #4) + spring hover (Pattern #7, restrained)
12. Manifest quote  → section reveal (Pattern #6)
13. Journal label/heading → section reveal (Pattern #6)
14. Journal cards   → stagger scroll reveal (Pattern #4) + spring hover (Pattern #7, restrained)
15. CTA section     → section reveal (Pattern #6)
16. Footer          → footer reveal (Pattern #8)
```

## Phase 2 — Implementation

### Stack Detection
- **Stack:** Vanilla HTML (plain `<script>` tags, Tailwind via CDN, no framework)
- **Cleanup pattern:** `gsap.matchMedia()` + cleanup return function

### CDN Dependencies Added
- `gsap@3.14/dist/gsap.min.js` (core)
- `gsap@3.14/dist/ScrollTrigger.min.js` (scroll reveals + parallax)
- `gsap@3.14/dist/SplitText.min.js` (hero heading kinetic typography)

### HTML Modifications
- Added semantic animation classes: `.hero-section`, `.hero-badge`, `.hero-heading`, `.hero-body`, `.hero-ctas`, `.hero-metrics`, `.hero-image`
- Added `.section-label`, `.section-heading`, `.section-body` classes to all sections
- Added `.reveal-card` class to all cards (rituals, products, journal)
- Added `.cta-section` to final CTA section
- Added `data-magnetic` attribute to CTA buttons
- **Removed** CSS `transition` from `.btn-sage` to avoid GSAP ownership conflict

### Motion Personality Adaptations (subtle)
All patterns were adapted to match the "breathing" brand feel:

| Default | Adapted for Wellness |
|---------|---------------------|
| `y: 40` entrance offset | `y: 15-30` (gentler) |
| `duration: 0.6` base | `duration: 0.7-1.0` (slower, unhurried) |
| `power3.out` impact easing | `power2.out` entrance easing (calmer) |
| `stagger: 0.09` medium | `stagger: 0.13` loose (breathing pace) |
| Spring hover `back.out(1.7)` | `power2.out` entrance (no bounce) |
| Card lift `y: -8, scale: 1.02` | `y: -5, scale: 1.015` (restrained) |
| Magnetic pull strength `0.35` | `0.2` (gentle gravitational pull) |
| Parallax `yPercent: -20` | `yPercent: -8` (subtle drift) |

### Patterns Implemented (9 total)
1. **Pattern #9 — SplitText Hero Heading:** Word-level mask reveal with `autoSplit`, `aria: true`, `yPercent: 100` entrance from below line clip. Duration 1.0s, stagger 0.08s.
2. **Pattern #1 — Hero Entrance Timeline:** 5 chained `.fromTo` calls for badge, body, CTAs, metrics, and hero image. Staggered delays with `"-=0.2"` to `"-=0.6"` overlaps.
3. **Pattern #5 — Parallax Scrub (Hero Image):** Desktop-only, `yPercent: -8` with `scrub: 1.5`. Subtle drift creating depth as user scrolls past hero.
4. **Pattern #2 — Smart Navbar:** Velocity-based hide on scroll-down (`yPercent: -100`), reveal on scroll-up (`yPercent: 0`). Direction-change debounced.
5. **Pattern #6 — Section Reveals:** All `.section-label`, `.section-heading`, `.section-body` elements reveal individually at `start: "top 88%"`.
6. **Pattern #4 — Card Stagger Reveal:** Cards grouped by parent section, staggered at 0.13s (loose) per card. `start: "top 88%"`.
7. **Pattern #7 — Spring Hover (Restrained):** Cards lift `y: -5` with `scale: 1.015` on mouseenter. Returns gently on mouseleave. No spring/elastic easing — uses `power2.out` for calm brand.
8. **Pattern #3 — Magnetic CTA (Desktop-Only):** Touch-guarded. Pull strength reduced to 0.2 for gentle gravitational feel.
9. **Pattern #8 — Footer Reveal:** Footer fades up from `y: 30` at `start: "top 95%"`.

## Phase 3 — Self-Verification

### Checklist Results
- [PASS] Hero timeline with 5+ chained `.fromTo` calls
- [PASS] ScrollTrigger scroll reveals on all 6 major sections
- [PASS] Interactive effect present (magnetic CTA, card hover)
- [PASS] `gsap.matchMedia()` wraps all animation code
- [PASS] `ScrollTrigger.refresh()` on `window.load`
- [PASS] `autoAlpha` used everywhere (never bare `opacity`)
- [PASS] No CSS `transition` conflicts (removed `.btn-sage` transition)
- [PASS] No deny-list properties animated
- [PASS] Cleanup function returns from matchMedia callback
- [PASS] Touch guard on magnetic buttons and parallax
- [PASS] `gsap.registerPlugin(ScrollTrigger, SplitText)` present
- [PASS] All `gsap.from` calls replaced with `gsap.fromTo` (no flash bug)
- [PASS] Pinned CDN version (`gsap@3.14`)
- [PASS] `prefers-reduced-motion: reduce` fallback sets `clearProps: "all"` on all elements

## Output Files
- `12-health-wellness-animated.html` — Full animated page (single file, no external dependencies beyond CDN)
- `transcript.md` — This file
- `metrics.json` — Tool call metrics
