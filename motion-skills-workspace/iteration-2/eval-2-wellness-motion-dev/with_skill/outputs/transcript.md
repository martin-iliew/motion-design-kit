# Motion-Dev Transcript: 12-health-wellness.html

## Task
Animate a wellness landing page with calm, nature-rooted motion that feels like breathing, not bouncing. Add scroll-triggered reveals for each section and subtle parallax on the hero.

---

## Phase 1 — Element Audit

### Site Context
- **Detected:** Marketing/wellness — single hero CTA, minimal nav, calm brand copy ("Nourish the self", "Quiet the noise"), nature-rooted imagery
- **Personality:** `subtle` — base/slow durations, entrance easing (power2.out), loose stagger (0.13s). NO spring or elastic easing to match the calm, breathing brand request.
- **Stack:** Vanilla HTML (GSAP + ScrollTrigger)

### Pattern Selection Notes
- **Text Scramble Decode** (badge.any #1): SKIPPED — trends-overview says "warm/calm brands: when NOT to use"
- **Magnetic Cursor Pull** (nav.any #1, button.any #1): SKIPPED — too energetic for wellness personality
- **Spring Physics** (card.any #1): REPLACED with gentle entrance easing — spring/elastic contradicts "not bouncing"
- **Parallax Depth Layers** (background.any #1): INCLUDED with reduced intensity (yPercent:-12 vs typical -20)

### Animation Plan

| # | Element | Pattern | Template | Guard | Notes |
|---|---------|---------|----------|-------|-------|
| 1 | Nav | Smart hide/show | #2 | — | Hides on scroll-down, shows on scroll-up |
| 2 | Hero badge | Hero timeline | #1 | prefersReduced | Gentle fade-up (no scramble — too aggressive) |
| 3 | Hero heading | Hero timeline | #1 | prefersReduced | Longer duration (1.0s / slow) for breathing feel |
| 4 | Hero body | Hero timeline | #1 | prefersReduced | Staggered cascade with overlap |
| 5 | Hero CTAs | Hero timeline + breathing pulse | #1 + CSS pulse | prefersReduced | Idle breathing animation on primary CTA |
| 6 | Hero stats | Hero timeline | #1 | prefersReduced | Final element in cascade |
| 7 | Hero image | Hero timeline + parallax | #1 + #5 | isTouch + prefersReduced | Scale-in entrance, then parallax scrub (desktop-only) |
| 8 | Rituals label | Section reveal | #6 | prefersReduced | Fade-up on scroll entry |
| 9 | Rituals heading | Section reveal | #6 | prefersReduced | Fade-up on scroll entry |
| 10 | Ritual cards (3) | Card stagger reveal + gentle hover | #4 + #7 variant | prefersReduced | Loose stagger (0.13s), hover lift y:-4 with entrance easing |
| 11 | Products label | Section reveal | #6 | prefersReduced | Fade-up on scroll entry |
| 12 | Products heading | Section reveal | #6 | prefersReduced | Fade-up on scroll entry |
| 13 | Product cards (4) | Card stagger reveal + gentle hover | #4 + #7 variant | prefersReduced | Same calm reveal pattern |
| 14 | Manifest quote | Section reveal | #6 | prefersReduced | Heading + attribution fade-up |
| 15 | Journal label | Section reveal | #6 | prefersReduced | Fade-up on scroll entry |
| 16 | Journal heading | Section reveal | #6 | prefersReduced | Fade-up on scroll entry |
| 17 | Journal cards (3) | Card stagger reveal + gentle hover | #4 + #7 variant | prefersReduced | Same calm reveal pattern |
| 18 | CTA section | Section reveal | #6 | prefersReduced | Heading + body + button fade-up |
| 19 | Footer | Footer reveal | #8 | prefersReduced | Reveals at 93% viewport entry |

**Total animated elements:** 19 groups across 7 GSAP patterns + 1 CSS pattern

---

## Phase 2 — Implementation Summary

### Patterns Used

| Pattern | Template # | Token Adjustments for Subtle Personality |
|---------|-----------|------------------------------------------|
| Hero Entrance Timeline | #1 | Duration: 0.7–1.0s (base–slow). Ease: power2.out (entrance). 6 chained fromTo calls. |
| Smart Navbar Hide/Show | #2 | Duration: 0.4s (fast). Ease: power2.in/out. Threshold at 100px. |
| Card Stagger Scroll Reveal | #4 | Duration: 0.65s (base). Stagger: 0.13s (loose). Start: top 88%. |
| Parallax Background Scrub | #5 | yPercent: -12 (reduced from -20). Scrub: 1.5. Desktop-only. |
| Section Label + Heading Reveal | #6 | Duration: 0.65–0.75s. Start: top 88%. Entrance easing. |
| Gentle Card Hover (Pattern 7 variant) | #7 | y: -4 (not -8). Scale: 1.01 (not 1.02). Ease: power2.out (no spring). |
| Footer Reveal | #8 | Duration: 0.8s. Start: top 93%. |
| Idle Breathing Pulse | CSS | Scale: 1.03. Cycle: 3.5s. Pauses on hover. |

### CSS Classes Added to HTML
- `.hero-section`, `.hero-badge`, `.hero-heading`, `.hero-body`, `.hero-ctas`, `.hero-stats`, `.hero-image` — for hero timeline targeting
- `.section-label`, `.section-heading`, `.section-body` — for section reveals
- `.reveal-card` — for card stagger + hover
- `.cta-primary` — for breathing pulse
- `.manifest-section`, `.cta-section` — for section scoping

### CDN Scripts Added
- `gsap@3.14/dist/gsap.min.js`
- `gsap@3.14/dist/ScrollTrigger.min.js`

### Plugins Registered
- `gsap.registerPlugin(ScrollTrigger)`

---

## Phase 3 — Self-Verify Results

| Check | Status | Detail |
|-------|--------|--------|
| Hero timeline 4+ chained calls | PASS | 6 chained .fromTo() calls (badge, heading, body, ctas, stats, image) |
| ScrollTrigger covers all sections | PASS | Rituals, Products, Manifest, Journal, CTA, Footer — all have scroll-triggered reveals |
| At least one interactive effect | PASS | Gentle card hover lift + idle breathing pulse on CTAs |
| gsap.matchMedia() used | PASS | mm.add("(prefers-reduced-motion: no-preference)") wraps everything |
| ScrollTrigger.refresh() on load | PASS | window.addEventListener("load", () => ScrollTrigger.refresh()) |
| autoAlpha (not bare opacity) | PASS | All fromTo calls use autoAlpha |
| No CSS transition conflict | PASS | Only background-color and color transitions remain — GSAP does not animate those |
| SPA cleanup | N/A | Vanilla multi-page HTML |
| Component isolation | N/A | No framework components |
| No deny-list properties | PASS | Only y, scale, autoAlpha, yPercent animated |
| gsap.registerPlugin() present | PASS | gsap.registerPlugin(ScrollTrigger) |
| No gsap.from() flash bug | PASS | All use fromTo with autoAlpha |

**All 10 applicable checks passed.**

---

## Key Design Decisions

1. **No spring/elastic easing anywhere** — user explicitly said "not bouncing". Used `power2.out` (entrance) everywhere for smooth, natural deceleration.
2. **Longer durations** — hero elements at 0.7–1.0s, section reveals at 0.65–0.75s. The "breathing" pace.
3. **Loose stagger (0.13s)** — cards reveal with gentle spacing, not rapid-fire.
4. **Reduced parallax intensity** — yPercent:-12 creates depth without drama.
5. **Idle breathing pulse** — the only continuous animation, applied only to primary CTAs, paused on hover.
6. **Text scramble skipped** — too tech/aggressive for a wellness brand.
7. **Magnetic cursor skipped** — too energetic; interactions are limited to gentle hover lifts.
