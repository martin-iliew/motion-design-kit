# Shared Guardrails

Load this reference for every `motion-build` and `motion-upgrade` run.

These rules are mode-independent.

---

## Stack Detection

Identify the target stack before writing code:

| Signal | Stack | Required cleanup pattern |
| --- | --- | --- |
| React / Next / Remix / TSX | React | `useGSAP({ scope })` with cleanup return |
| Vue / Nuxt / `.vue` / `<script setup>` | Vue 3 | `gsap.context()` inside `onMounted`, `ctx.revert()` in `onUnmounted` |
| Tailwind utilities without framework signal | Tailwind CSS | `motion-safe:` and `motion-reduce:` variants |
| `.html` / inline `<script>` / plain JS | Vanilla HTML | `gsap.matchMedia()` with cleanup return |
| CSS-only request | Vanilla CSS | `@media (prefers-reduced-motion: reduce)` fallback |

Load `references/stack-patterns.md` after detection when a scaffold is needed.

---

## Hard Rules

1. Reduced-motion handling is mandatory.
2. Use GPU-safe properties only: `x`, `y`, `xPercent`, `yPercent`, `scale`, `rotation`, `opacity`, `autoAlpha`.
3. Do not animate layout-triggering properties: `width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding`, `font-size`, `border-width`.
4. Register GSAP plugins before use.
5. GSAP plugins are free on current versions; never claim a membership requirement.
6. If a plugin or API detail is uncertain, fetch the official GSAP LLM reference once and reuse it.
7. Remove CSS `transition` on any property GSAP will own.
8. Use `fromTo` or `set` plus `to` on hidden elements. Do not use bare `from()` on opacity-hidden elements.
9. Use `autoAlpha` instead of bare `opacity` for GSAP entrance work.
10. Use `gsap.quickTo()` for pointer-heavy motion such as magnetic or cursor interactions.
11. Apply `will-change` dynamically and clear it after the interaction or scroll effect settles.

---

## Cleanup Rules

### Vanilla HTML

- Wrap animation work in `gsap.matchMedia()`.
- Return cleanup from the `no-preference` branch.
- For page-level work, call `ScrollTrigger.refresh()` on `window.load`.

### React

- Register plugins at module scope.
- Use `useGSAP` instead of bare `useEffect` or `useLayoutEffect` for GSAP orchestration.
- Scope selectors to the component root.
- Kill timelines and triggers in the cleanup return.

### Vue 3

- Register plugins at module scope.
- Use `gsap.context()` scoped to the component root.
- Revert the context in `onUnmounted`.

### CSS-only

- Provide visible, static reduced-motion output.
- Prefer browser-native scroll animation support with a safe fallback when relevant.

---

## SPA and Multi-Page Safety

If the project uses a client-side router, route changes must kill all timelines and `ScrollTrigger` instances created by that screen or component.

Router signals:

- `react-router`, `@remix-run/react`, `next/navigation`
- `vue-router`, `RouterView`
- `astro:page-load`, `astro:before-swap`
- transition libraries such as `barba`, `swup`, or `Highway`

Component isolation is mandatory:

- React and Vue components may animate only inside their own DOM subtree.
- Do not share one global timeline across unrelated components.

For traditional multi-page sites, shared motion helpers must accept a container and scope selectors to it.

---

## Safe Substitutions

If the request asks for a layout-triggering animation, substitute the GPU-safe equivalent and explain the change:

| Requested property | Safe substitute |
| --- | --- |
| `width` | `scaleX` |
| `height` | `scaleY` |
| `top` / `bottom` | `y` / `yPercent` |
| `left` / `right` | `x` / `xPercent` |
| `font-size` | `scale` on a wrapper |
| `margin` / `padding` | translate via `x` or `y` |

---

## Self-Verification

Before stopping:

- [ ] Reduced-motion handling exists and matches the stack
- [ ] No layout-triggering properties are animated
- [ ] Cleanup and plugin registration match the stack
- [ ] No CSS transition conflicts remain
- [ ] Hidden-element entrances use `autoAlpha` / `fromTo` correctly
- [ ] Page-level work refreshes `ScrollTrigger` on load when needed
- [ ] SPA/router cleanup is wired where applicable
- [ ] Component scope is respected in framework stacks

Extra page-level checks for hero-led work:

- [ ] Hero timeline has 4+ distinct chained tween calls when the hero contains enough visible groups to support it
- [ ] Major sections receive scroll-reveal coverage
- [ ] At least one interaction effect exists in `balanced` or `premium`, or in `fast` when it is a direct user requirement
