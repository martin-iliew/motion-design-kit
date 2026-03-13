# Motion Guardrails

Load this reference for every `motion-build` and `motion-upgrade` run.

## Stack Detection

Identify the target stack before writing code:

| Signal | Stack | Required cleanup pattern |
| --- | --- | --- |
| React / Next / Remix / TSX | React | `useGSAP({ scope })` with cleanup return |
| Vue / Nuxt / `.vue` / `<script setup>` | Vue 3 | `gsap.context()` inside `onMounted`, `ctx.revert()` in `onUnmounted` |
| Tailwind utilities without framework signal | Tailwind CSS | `motion-safe:` and `motion-reduce:` variants |
| `.html` / inline `<script>` / plain JS | Vanilla HTML | `gsap.matchMedia()` with cleanup return |
| CSS-only request | Vanilla CSS | `@media (prefers-reduced-motion: reduce)` fallback |

## Hard Rules

1. Reduced-motion handling is mandatory.
2. Only GPU-safe properties may be animated.
3. Do not animate layout-triggering properties.
4. Remove CSS transitions from GSAP-owned properties.
5. Use `fromTo` or `autoAlpha` correctly for hidden elements.
6. Respect `brief/motion-hints.yaml` family and intensity limits.
7. Use token-derived timing and easing values instead of raw literals when the project exposes them.
8. Do not animate elements missing from the design decision pack.

## Cleanup Rules

- Vanilla HTML: `gsap.matchMedia()` with cleanup return
- React: `useGSAP` scoped to the component root
- Vue 3: `gsap.context()` and `ctx.revert()` on unmount
- CSS-only: visible reduced-motion fallback

## Self-Verification

- [ ] reduced-motion exists and matches the stack
- [ ] cleanup matches the stack
- [ ] no banned properties are animated
- [ ] selected motion families are allowed by the design handoff
- [ ] the page remains usable without the animation layer
