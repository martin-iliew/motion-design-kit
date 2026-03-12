# Animation Transcript: SOLL Wellness Landing Page (Without Skill)

## Step 1: Analyze the Input HTML
- Read `12-health-wellness.html` (235 lines)
- Identified a calm, nature-rooted wellness brand (SOLL) with sections: Nav, Hero, Rituals (3 cards), Products (4 cards), Manifest/Quote, Journal (3 cards), CTA, Footer
- Noted the page uses Tailwind CSS v4 (browser build) + Cormorant Garamond + Inter fonts
- No existing animations beyond hover transitions (`btn-sage`, `link-sage`)
- Color palette: sage green, clay, sand, linen -- all soft earth tones

## Step 2: Determine Animation Strategy
- **Brand feel:** "like breathing, not bouncing" -- calm, slow, nature-rooted
- **Library choice:** GSAP 3.12.5 + ScrollTrigger (CDN)
- **Easing philosophy:** `power2.out` as primary ease -- gentle deceleration like an exhale. `power1.inOut` for the quote section for meditative symmetry
- **Duration range:** 0.6s - 1.4s (longer than typical web animations to match brand calm)
- **Transform distance:** 20-40px vertical movement -- subtle, not dramatic
- **Accessibility:** `gsap.matchMedia()` wrapping all animations with `prefers-reduced-motion` support

## Step 3: Add GSAP + ScrollTrigger CDN Scripts
- Added `gsap.min.js` and `ScrollTrigger.min.js` from cdnjs (v3.12.5) in `<head>`
- Registered ScrollTrigger plugin at script start
- Added `ScrollTrigger.refresh()` on window load to account for Tailwind/font settling

## Step 4: Add Data Attributes for Animation Targeting
- Added `data-animate="..."` attributes to all animatable elements throughout the HTML
- Naming convention: `section-element` (e.g., `hero-title`, `ritual-card`, `products-tag`)
- Total: ~30 data-animate attributes across all sections

## Step 5: Implement Nav Animation (Load-Triggered)
- Logo slides in from left with fade (0.8s)
- Nav links stagger down with fade (0.6s each, 0.08s stagger)
- CTA button scales in with fade (0.7s)
- Timeline starts after 0.1s delay

## Step 6: Implement Hero Animation (Load-Triggered)
- Staggered timeline starting at 0.3s delay:
  - Tag line fades up (0.8s)
  - Main heading "Nourish the self / Quiet the noise" fades up (1.2s -- longest for emphasis)
  - Body text fades up (1.0s)
  - Button group fades up (0.9s)
  - Stats bar fades up (0.9s)
  - Hero image fades in with scale from 0.97 + upward drift (1.4s -- the grandest entrance)
- Each element overlaps the previous by 0.5-0.7s for a flowing, breathing cadence

## Step 7: Implement Hero Parallax
- Hero image gets a subtle vertical parallax: drifts 50px upward as user scrolls past the hero section
- `scrub: 1.2` for smooth, slightly lagged tracking (feels organic, not mechanical)
- Only active on desktop (no parallax in reduced-motion mode)

## Step 8: Create Reusable scrollReveal Helper
- Factory function accepting selector + options (y, scale, duration, stagger, start, delay)
- Uses `autoAlpha` (not bare opacity) for GPU compositing + proper visibility toggle
- Default trigger start: `top 85%` (reveals slightly before element reaches viewport center)
- All values branch on `isDesktop` vs `isReduced` from matchMedia

## Step 9: Implement Rituals Section (Scroll-Triggered)
- Section tag, heading, and link fade up individually
- 3 ritual cards stagger in (0.15s apart) with y: 36px + scale: 0.97
- Duration: 1.0s per card

## Step 10: Implement Products Section (Scroll-Triggered)
- Section tag and heading fade up
- 4 product cards stagger in (0.12s apart) with y: 30px + scale: 0.97
- Duration: 0.9s per card

## Step 11: Implement Manifest/Quote Section (Scroll-Triggered)
- Quote text uses `power1.inOut` easing (symmetrical, meditative) with scale from 0.94
- Duration: 1.4s -- the slowest reveal on the page, matching the contemplative content
- Attribution fades up 0.6s after quote begins

## Step 12: Implement Journal Section (Scroll-Triggered)
- Same pattern as Rituals: tag, heading, link fade up, then 3 cards stagger in
- Cards: 0.15s stagger, 1.0s duration, y: 36px + scale: 0.97

## Step 13: Implement CTA Section (Scroll-Triggered)
- Heading fades up (1.0s)
- Body text fades up (0.8s)
- Button uses `back.out(1.2)` -- the *only* slightly springy ease on the page, for the primary action
- "No card required" note fades in last (0.6s)

## Step 14: Implement Footer (Scroll-Triggered)
- Brand block fades up (0.8s)
- 3 footer columns stagger in (0.1s apart, 0.7s each)
- Bottom bar (copyright/links) fades in last (0.6s)
- Trigger starts at `top 90%` (footer is usually visible quickly)

## Step 15: Verify Output
- Confirmed outputs directory was created
- Wrote final HTML file (single self-contained file with embedded GSAP script)
- All original HTML structure preserved; only additions are data attributes and the animation script block

## Animation Summary
| Section    | Type           | Duration Range | Ease           | Special          |
|-----------|----------------|----------------|----------------|------------------|
| Nav       | Load timeline  | 0.6-0.8s       | power2.out     | Stagger links    |
| Hero      | Load timeline  | 0.8-1.4s       | power2.out     | Parallax image   |
| Rituals   | Scroll reveal  | 0.7-1.0s       | power2.out     | 3-card stagger   |
| Products  | Scroll reveal  | 0.7-0.9s       | power2.out     | 4-card stagger   |
| Manifest  | Scroll reveal  | 0.8-1.4s       | power1.inOut   | Scale from 0.94  |
| Journal   | Scroll reveal  | 0.7-1.0s       | power2.out     | 3-card stagger   |
| CTA       | Scroll reveal  | 0.6-1.0s       | power2.out     | back.out button  |
| Footer    | Scroll reveal  | 0.6-0.8s       | power2.out     | Column stagger   |

## Key Technical Decisions
- **autoAlpha** used everywhere instead of bare `opacity` (GPU-composited, sets `visibility: hidden` when 0)
- **gsap.matchMedia()** wraps everything for `prefers-reduced-motion` support
- **No CSS keyframes** added -- all motion via GSAP for single source of truth
- **ScrollTrigger.refresh()** on window load to handle Tailwind CSS runtime settling
- **toggleActions: "play none none none"** -- animations play once, no replay on scroll back (calmer UX)
- **No GSAP plugins beyond ScrollTrigger** -- no SplitText, no MotionPath, keeping it minimal
