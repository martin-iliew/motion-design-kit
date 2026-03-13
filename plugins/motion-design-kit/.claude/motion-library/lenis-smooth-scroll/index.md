# Lenis Smooth Scroll Integration

**Framework:** Lenis + GSAP ScrollTrigger
**Category:** scroll
**2026 Relevance:** Lenis has become the 2025-2026 standard for smooth scrolling, replacing Locomotive Scroll and other older libraries. It provides butter-smooth momentum scrolling with minimal bundle size (~4KB gzipped) and clean integration with GSAP ScrollTrigger. Adopted by major agencies and studios worldwide.

## Description

Lenis intercepts native scroll events and applies momentum-based inertia with configurable duration and easing. When paired with GSAP ScrollTrigger, Lenis handles the scroll feel while ScrollTrigger handles animation logic. Synchronization is achieved by piping Lenis scroll events into `ScrollTrigger.update()` and adding the Lenis RAF loop to GSAP's ticker.

## Do's

- Connect Lenis to GSAP via `lenis.on("scroll", ScrollTrigger.update)` and `gsap.ticker.add()`
- Disable GSAP's lag smoothing with `gsap.ticker.lagSmoothing(0)` for Lenis compatibility
- Destroy Lenis instance when `prefers-reduced-motion: reduce` is active
- Use pinned GSAP version with Lenis — test compatibility when upgrading either library
- Call `lenis.destroy()` on SPA unmount to prevent memory leaks

## Don'ts

- Don't use Lenis on dashboards, data tables, or forms — smooth scrolling interferes with precise input
- Don't combine with CSS `scroll-behavior: smooth` — they conflict
- Don't use on mobile-only sites — Lenis' momentum scrolling can feel unnatural on touch devices with native inertia
- Don't set `duration` above 2.0 — it makes the page feel sluggish and unresponsive
