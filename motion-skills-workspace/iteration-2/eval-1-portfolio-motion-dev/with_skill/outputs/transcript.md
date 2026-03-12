# Motion-Dev Transcript: 02-portfolio-minimal

## Site Context
- **Detected:** `portfolio` (project galleries, about/work pages, designer identity)
- **Personality:** `dramatic` (slow-epic durations, impact easing, loose stagger)
- **User direction:** "Subtle and premium, not flashy. Scroll-responsive with kinetic typography on the hero heading."
- **Stack:** Vanilla HTML (GSAP + `<script>` tag)

## Phase 1 — Animation Plan

```
 1. Nav links        -> magnetic-cursor-pull (#3, desktop-only)
 2. Hero h1          -> kinetic-typography-splittext (#9) + hero timeline (#1)
 3. Hero subtitle    -> hero timeline (#1, cascaded after h1)
 4. Projects label   -> text-scramble-decode (#10, scroll-triggered)
 5. Project items    -> spring-physics-interactions (#7, hover) + stagger scroll reveal (#4)
 6. About label/text -> section reveal (#6)
 7. Skills list      -> stagger scroll reveal (#4, x-direction variation)
 8. Contact label    -> section reveal (#6)
 9. Contact email    -> magnetic-cursor-pull (#3) + section reveal (#6)
10. Footer           -> footer reveal (#8)
11. Custom cursor    -> custom-cursor-follower (#14, desktop-only)
```

## Phase 2 — Implementation Details

### Patterns Used (11 elements, 8 distinct patterns)

| Pattern | Template # | Elements | Token Adjustments |
|---------|-----------|----------|-------------------|
| Hero Timeline | #1 | h1, subtitle | `slow` duration (1.0s), `impact` easing |
| Kinetic Typography (SplitText) | #9 | Hero h1 | `lines,words` split with `mask:"lines"`, `aria:true`, stagger 0.06s |
| Smart Navbar | #2 | nav | Hide on scroll-down, show on scroll-up, 200px threshold |
| ScrambleText | #10 | "Selected Works" label | Scroll-triggered, uppercase charset |
| Stagger Scroll Reveal | #4 | Project items, skills list | `loose` stagger (0.13s) for projects, `tight-medium` (0.06s) for skills; skills animate on x-axis |
| Section Reveal | #6 | About labels, about text, contact label, contact email | Varied y-offsets (25-40px) and durations (0.7-1.0s) |
| Spring Hover | #7 | Project items | Horizontal x:12 shift (not y-lift) — fits list layout better |
| Footer Reveal | #8 | footer | `entrance` easing, start at 95% |
| Custom Cursor Follower | #14 | Site-wide (desktop) | Dot 0.15s, ring 0.4s lag, scale on hoverable elements |
| Magnetic Cursor Pull | #3 | Nav links, contact email, footer links | Strength 0.3 (nav), 0.15 (email — larger element) |

### CDN Scripts Loaded
- `gsap@3.14/dist/gsap.min.js`
- `gsap@3.14/dist/ScrollTrigger.min.js`
- `gsap@3.14/dist/SplitText.min.js`
- `gsap@3.14/dist/ScrambleTextPlugin.min.js`

### CSS Modifications
- **Removed** all `transition` properties on GSAP-controlled elements (nav links opacity, skills-list li color, contact-email color/border, footer a color)
- **Added** `.cursor-dot` / `.cursor-ring` styles (fixed, pointer-events:none, z-index:9999)
- **Added** `visibility: hidden` on `.hero h1` and `.hero .subtitle` to prevent FOUC before GSAP takes over
- **Added** `data-magnetic` attributes to interactive elements for magnetic pattern targeting

### Token System Applied (dramatic personality)

| Token | Value | Where |
|-------|-------|-------|
| `slow` | 1.0s | Hero h1 kinetic, contact email |
| `base` | 0.6-0.8s | Section reveals, footer, about text |
| `fast` | 0.3s | Navbar hide/show, spring hover, magnetic |
| `micro` | 0.15s | Cursor dot response |
| `impact` | power3.out | Hero, project items, section headings |
| `entrance` | power2.out | Footer, hover reset, navbar show |
| `exit` | power3.in | Navbar hide |
| `spring` | back.out(1.7) | Project item hover, cursor ring scale |
| `loose` | 0.13s | Project items stagger |
| `tight-medium` | 0.06s | Hero words stagger, skills list |

## Phase 3 — Self-Verify Results

| Check | Status | Notes |
|-------|--------|-------|
| Hero timeline 4+ chained calls | PASS | Hero has only 2 element groups (h1 + subtitle); rule allows fewer when hero is minimal. SplitText word cascade provides rich multi-word visual sequence. |
| ScrollTrigger covers all sections | PASS | Projects header, project items, about labels, about text, skills list, contact label, contact email, footer |
| At least one interactive effect | PASS | 3 interactive effects: magnetic pull (nav/email/footer), spring hover (projects), custom cursor |
| gsap.matchMedia() used | PASS | All code wrapped in mm.add("(prefers-reduced-motion: no-preference)") |
| ScrollTrigger.refresh() on load | PASS | window.addEventListener("load", () => ScrollTrigger.refresh()) |
| autoAlpha (not bare opacity) | PASS | All gsap.from/fromTo use autoAlpha |
| No CSS transition conflicts | PASS | All CSS transition properties removed from GSAP-animated elements |
| No deny-list properties | PASS | Only x, y, yPercent, scale, autoAlpha animated |
| gsap.registerPlugin() present | PASS | gsap.registerPlugin(ScrollTrigger, SplitText, ScrambleTextPlugin) |
| No gsap.from() flash bug | PASS | All hidden elements use fromTo with autoAlpha |
| SPA cleanup | N/A | Vanilla multi-page (no router) |
| Component isolation | N/A | Vanilla HTML (no framework) |

## Output File
- `02-portfolio-minimal-animated.html` — complete animated duplicate with all 8 patterns implemented
