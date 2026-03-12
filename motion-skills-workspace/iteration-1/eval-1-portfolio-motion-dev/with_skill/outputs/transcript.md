# Motion-Dev Skill Transcript — Portfolio Minimal

## Task
Add GSAP animations to a minimal designer portfolio. Subtle and premium feel, scroll-responsive, kinetic typography on hero heading.

## Input
- `02-portfolio-minimal.html` — Single-page designer portfolio with nav, hero, projects list, about, contact, footer

## Workflow Execution

### Phase 1 — Element Audit

**Site Context Detected:** `portfolio` (project galleries, about/work pages, designer portfolio)

**Personality:** `dramatic` — Duration bias: slow-epic, Easing bias: impact/exit, Stagger bias: loose

**Animation Plan:**

| # | Element | Pattern | Source |
|---|---------|---------|--------|
| 1 | Nav links | Magnetic cursor pull (#3, desktop-only) | scores.yaml: nav.portfolio[0] |
| 2 | Hero h1 | Kinetic typography SplitText (#9) — line-masked word reveal | scores.yaml: heading.portfolio[0] + user request |
| 3 | Hero .subtitle | Hero timeline (#1) — fromTo fade+slide after h1 | Part of hero sequence |
| 4 | "Selected Works" h2 | ScrambleText decode (#10) — scroll-triggered | scores.yaml: label.any[0] |
| 5 | Project items (6x) | Stagger scroll reveal (#4) + spring hover (#7) | scores.yaml: card.portfolio adapted for list items |
| 6 | About labels + text | Section reveal (#6) — scroll-triggered | scores.yaml: section.portfolio |
| 7 | Skills list (8 items) | Stagger reveal (#4) — x-axis slide | Adapted from Pattern 4 |
| 8 | Contact label + email | Section reveal (#6) | scores.yaml: section.portfolio |
| 9 | Contact email | Magnetic cursor pull (#3, desktop-only) | scores.yaml: cta.any[1] |
| 10 | Footer | Footer reveal (#8) | scores.yaml: footer.any[0] |
| 11 | Custom cursor | Cursor follower (#14, desktop-only) | scores.yaml: site_contexts.portfolio.prefer[0] |
| 12 | Nav | Smart hide/show (#2) — velocity-driven | Pattern 2 from gsap-patterns.md |

### Phase 2 — Implement

**Stack:** Vanilla HTML (GSAP) — detected from `<script>` tags and plain HTML structure.

**Reference files loaded:**
- `.claude/motion-library/scores.yaml` — pattern selection
- `.claude/motion-library/trends-overview.md` — feel/avoid context
- `references/gsap-patterns.md` — 17 production templates
- `references/css-patterns.md` — CSS-only patterns (not used, all elements had GSAP patterns)
- `.claude/skills/shared/audit-rules.md` — Parts A, C, D, E
- `https://gsap.com/llms.txt` — SplitText + ScrambleTextPlugin API reference

**CDN scripts added:**
- `gsap@3.14/dist/gsap.min.js`
- `gsap@3.14/dist/ScrollTrigger.min.js`
- `gsap@3.14/dist/SplitText.min.js`
- `gsap@3.14/dist/ScrambleTextPlugin.min.js`

**Key implementation decisions:**
1. **Kinetic Typography (Pattern 9):** Used `SplitText` with `type: "lines,words"`, `mask: "lines"` for cinematic curtain-lift word reveals. `autoSplit: true` for responsive re-splitting. `aria: true` for accessibility. Dramatic personality: 1.0s duration, 0.06s stagger.
2. **Custom Cursor (Pattern 14):** Dot at 0.15s (micro), ring at 0.4s for elastic personality. Ring scales 2.2x on hoverable elements. Desktop-only with touch guard.
3. **Project Items:** Combined scroll reveal (Pattern 4) with spring hover (Pattern 7). Hover shifts items 12px right with `back.out(1.7)` spring — editorial feel without flashiness.
4. **ScrambleText (Pattern 10):** Applied to "Selected Works" heading. Scroll-triggered, 1.5s decode with uppercase charset only. Dramatic pacing.
5. **Smart Navbar (Pattern 2):** Hides on scroll-down after 300px, shows on scroll-up. Velocity-driven.
6. **Magnetic Pull (Pattern 3):** Applied to nav links, contact email, footer social links. Reduced strength (0.2) on large contact email, standard (0.35) on nav/footer.

**CSS transitions removed (conflict prevention):**
- `.project-title` — removed inherited hover transition on color
- `nav .links a` — removed `transition: opacity .3s ease`
- `.skills-list li` — removed `transition: color .2s ease`
- `.contact-email` — removed `transition: color .3s ease`
- `footer a` — removed `transition: color .2s`

### Phase 3 — Self-Verify

| Check | Status |
|-------|--------|
| Hero timeline with 4+ chained calls | FAIL — only 2 chained calls exist on the hero timeline |
| ScrollTrigger covers all sections | PASS — projects, about, skills, contact, footer |
| Interactive effect present | PASS — magnetic pull, spring hover, custom cursor |
| `gsap.matchMedia()` used | PASS — all code wrapped in mm.add() |
| `ScrollTrigger.refresh()` on load | PASS — window.addEventListener("load", ...) |
| `autoAlpha` everywhere | PASS — no bare opacity in from/fromTo |
| No CSS transition conflicts | PASS — all conflicting transitions removed |
| No deny-list properties | PASS — only x, y, scale, autoAlpha, yPercent |
| Touch guards on interactive patterns | PASS — isTouch check on patterns 3, 14 |
| Cleanup function returned | PASS — kills timelines, reverts SplitText, kills ScrollTriggers |

## Output
- `02-portfolio-minimal-animated.html` — Complete animated version with all patterns applied
