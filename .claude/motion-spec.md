# Motion Spec

A **Motion Spec** is a stack-agnostic YAML document that fully describes a single animation unit. It captures animation intent in a language-neutral way that any output target can read: vanilla CSS, GSAP, Web Animations API, Rive, Lottie, WebGL, or anything else.

Motion Spec is used by the `motion-dev` skill when translating animations between stacks, and by the `motion-discover` command when generating new pattern files. You can ask "show me the spec" for any animation to get the canonical representation.

All token values (`duration`, `easing`, `stagger.tier`) resolve against [motion-tokens.md](./motion-tokens.md).

---

## Design Principles

- **Language-neutral**: A Motion Spec describes _what_ animates, not _how_ a specific library does it. Anyone familiar with web animation — CSS or GSAP or anything else — should be able to read it.
- **Flexible field model**: Include what applies, skip what doesn't. Fields are optional and context-dependent. Only four fields are universally required.
- **Open type system**: The `type` field is a free-form string. Known conventions are `tween`, `procedural`, and `browser-native`, but `webgl`, `rive`, `lottie`, `houdini`, and any future type are valid without a schema update.
- **Extensible**: New fields can be freely added for new pattern types. An `motion-dev` translator that encounters an unknown field should pass it through or ignore it gracefully.

---

## Universally Required Fields

Every Motion Spec, regardless of type, must include these four fields:

```yaml
version: "1" # Schema version — increment only on breaking changes
type: string # Free-form: "tween" | "procedural" | "browser-native" | any future type
id: string # Kebab-case identifier, e.g. "hero-title-reveal"
a11y:
  reduced_motion: skip | instant-final | instant-start
```

All other fields are optional and context-dependent. Include what applies to the animation; omit what doesn't.

---

## Field Reference

### `version`

Always `"1"`. Increment only on a breaking schema change.

### `type`

Free-form string identifying the animation pattern family. Known values:

| Value            | Meaning                                                                     |
| ---------------- | --------------------------------------------------------------------------- |
| `tween`          | A keyframe-based from/to animation with explicit timing                     |
| `procedural`     | Physics-driven or generative motion (springs, particles, noise)             |
| `browser-native` | Uses Web Animations API, CSS `@keyframes`, or `animation-timeline` directly |

Future types — `webgl`, `rive`, `lottie`, `houdini`, etc. — are valid without any schema update.

### `id`

Kebab-case string uniquely identifying this pattern, e.g. `"hero-title-reveal"`, `"feature-cards-stagger"`.

### `target`

What gets animated.

```yaml
target:
  selector: string # CSS selector — stack-agnostic, e.g. ".hero-title"
  type: element | group # element = single node, group = querySelectorAll + stagger
```

### `from` / `to`

Start and end states. Only include fields that differ from the element's natural state. All properties must be GPU-safe (see motion-tokens.md allow-list).

```yaml
from:
  opacity: number # 0–1
  x: number # px → translateX (use instead of left/right)
  y: number # px → translateY (use instead of top/bottom)
  xPercent: number # % → translateX(n%)
  yPercent: number # % → translateY(n%)
  scale: number # uniform scale (use instead of width/height)
  scaleX: number # horizontal scale only
  scaleY: number # vertical scale only
  rotation: number # degrees
  rotationX: number # 3D perspective flip (requires perspective on parent)
  rotationY: number
  skewX: number
  skewY: number

to:
  # same shape as "from" — only list changed fields
```

### `timing`

Controls duration and easing. Use token names wherever possible; use `_raw` overrides only when a token doesn't fit.

```yaml
timing:
  duration: micro | fast | base | slow | epic # token — resolves via motion-tokens.md
  duration_raw: number # seconds — overrides token when needed
  easing: entrance | impact | transition | exit | spring | elastic | scrub | brand
  easing_raw: string # CSS cubic-bezier(...) syntax ONLY — see note below
  delay: number # seconds, optional
```

**`easing_raw` syntax rule:** Must use CSS `cubic-bezier(x1, y1, x2, y2)` notation. GSAP function names like `elastic.out(1, 0.3)` are not valid here — they are implementation details, not portable descriptions. When approximating elastic easing in a raw override, use a CSS cubic-bezier value (e.g. `cubic-bezier(0.34, 1.8, 0.64, 1)` for a mild elastic pop). For true multi-oscillation springs, use the `procedural` type instead.

**Token resolution note:** Easing tokens resolve to their CSS `cubic-bezier` equivalents — see the [Token Resolution](#token-resolution) section and motion-tokens.md.

### `stagger`

Only relevant when `target.type` is `group`.

```yaml
stagger:
  tier: tight | medium | loose # token — resolves via motion-tokens.md
  value_raw: number # per-element seconds — overrides token when needed
  from: start | center | end | random | edges # stagger direction
```

### `trigger`

What initiates the animation.

```yaml
trigger:
  type: load | scroll | hover | click | focus | state-change | manual
  # scroll-specific:
  scroll_start: string # e.g. "top 80%" — viewport entry point
  scroll_end: string # e.g. "bottom 20%"
  scroll_scrub: boolean | number # false = play-once, true = hard scrub, 0.5–2 = smooth scrub
  scroll_pin: boolean # pin trigger element during animation
  toggle_actions: string # e.g. "play none none reverse"
  # interaction-specific:
  event_target: string # selector for the element receiving the event (if different from animated element)
```

### `physics`

Optional fine-tuning for procedural/spring animations. Expresses spring parameters in a framework-neutral way — translators map these to their target's spring model.

```yaml
physics:
  type: spring
  stiffness: number # spring stiffness (high = snappy, low = loose); maps to GSAP period inversely
  damping: number # resistance (high = no overshoot, low = oscillation); maps to GSAP amplitude inversely
  mass: number # simulated mass (affects inertia); optional
```

> **Note on the old `amplitude`/`period` fields:** Earlier versions of this spec used GSAP's `elastic.out(amplitude, period)` parameter names. Those are replaced by `stiffness`/`damping`/`mass` — framework-neutral terms. Translators targeting GSAP should map: `stiffness → 1/period`, `damping → amplitude` (approximately).

### `sequence`

Timing hint for use inside a multi-animation timeline.

```yaml
sequence:
  position: string # Relative position: "-=0.3", "<0.2", "+=0.5", or a named label
```

### `a11y`

**Required on every spec.** Declares how this animation behaves when `prefers-reduced-motion: reduce` is active.

```yaml
a11y:
  reduced_motion: skip | instant-final | instant-start
  # skip          — do nothing (decorative, non-informational motion only)
  # instant-final — jump to "to" state immediately (DEFAULT for reveals and entrances)
  # instant-start — jump to "from" state immediately (for exit/hiding animations)
```

---

## Adding Fields for New Pattern Types

Motion Spec is intentionally open-ended. If a new pattern type needs fields not listed above, add them directly to the spec file with a comment explaining their meaning. No schema update is required. Example for a hypothetical `rive` type:

```yaml
version: "1"
type: rive
id: "mascot-wave"
a11y:
  reduced_motion: skip
rive:
  src: "/animations/mascot.riv"
  artboard: "Wave"
  state_machine: "Interaction"
  input: "trigger_wave"
```

---

## Three Complete Examples

### Pattern 1 — Tween (scroll-triggered reveal)

```yaml
version: "1"
type: tween
id: "hero-title-reveal"
target:
  selector: ".hero-title"
  type: element
from:
  opacity: 0
  y: 40
to:
  opacity: 1
  y: 0
timing:
  duration: base
  easing: entrance
trigger:
  type: scroll
  scroll_start: "top 80%"
  toggle_actions: "play none none reverse"
a11y:
  reduced_motion: instant-final
```

### Pattern 2 — Procedural (spring hover interaction)

```yaml
version: "1"
type: procedural
id: "button-spring-press"
target:
  selector: ".btn-primary"
  type: element
from:
  scale: 1
to:
  scale: 0.93
timing:
  duration: micro
  easing: exit
physics:
  type: spring
  stiffness: 400
  damping: 20
trigger:
  type: hover
  toggle_actions: "play none none reverse"
a11y:
  reduced_motion: skip
```

### Pattern 3 — Browser-Native (CSS scroll-driven animation)

```yaml
version: "1"
type: browser-native
id: "progress-bar-scroll"
target:
  selector: "#reading-progress"
  type: element
timing:
  easing: scrub
trigger:
  type: scroll
  scroll_scrub: true
browser_native:
  animation_timeline: "scroll(root block)"
  animation_range: "0% 100%"
  keyframes:
    - offset: 0
      scaleX: 0
    - offset: 1
      scaleX: 1
a11y:
  reduced_motion: instant-final
```

---

## Token Resolution

When a translator reads a Motion Spec, it resolves token names from [motion-tokens.md](./motion-tokens.md). All easing tokens resolve to CSS `cubic-bezier` values — these are the portable, code-agnostic form. Framework-specific strings (like GSAP's `"power2.out"`) are implementation details that translators apply internally.

| Spec field                | Token      | CSS value                                            | GSAP equivalent               |
| ------------------------- | ---------- | ---------------------------------------------------- | ----------------------------- |
| `timing.duration: base`   | `base`     | `600ms`                                              | `duration: 0.6`               |
| `timing.easing: entrance` | `entrance` | `cubic-bezier(0.0, 0.0, 0.2, 1)`                     | `ease: "power2.out"`          |
| `timing.easing: spring`   | `spring`   | `cubic-bezier(0.34, 1.56, 0.64, 1)`                  | `ease: "back.out(1.7)"`       |
| `timing.easing: elastic`  | `elastic`  | `cubic-bezier(0.34, 1.8, 0.64, 1)` _(approximation)_ | `ease: "elastic.out(1, 0.3)"` |
| `stagger.tier: medium`    | `medium`   | `calc(var(--i) * 90ms)`                              | `stagger: { each: 0.09 }`     |

**Raw override precedence:** `duration_raw` overrides `duration` token. `easing_raw` overrides `easing` token. Always add an inline comment when using a raw override explaining why the token doesn't fit.

---

## GPU-Safe Property Constraint

The `from` and `to` blocks accept **only** properties from the GPU-safe allow-list in motion-tokens.md. If an animation requires a deny-list property, substitute the safe equivalent:

| Requested                | Safe substitute                                        |
| ------------------------ | ------------------------------------------------------ |
| `width: 0 → 300px`       | `scaleX: 0 → 1` (add `transformOrigin: "left center"`) |
| `height: 0 → auto`       | `scaleY: 0 → 1` (add `transformOrigin: "top center"`)  |
| `top: -50px → 0`         | `y: -50 → 0`                                           |
| `left: -100% → 0`        | `xPercent: -100 → 0`                                   |
| `font-size: 12px → 24px` | `scale: 0.5 → 1` on the text container                 |

---

## Translation Targets Summary

Full translation rules live in `skills/motion-dev/references/motion-spec-translation-guide.md`. This table shows which spec fields each target uses:

| Spec field                | Vanilla CSS                               | Tailwind                   | GSAP HTML            | GSAP React            | GSAP Vue             |
| ------------------------- | ----------------------------------------- | -------------------------- | -------------------- | --------------------- | -------------------- |
| `from`/`to`               | `@keyframes`                              | `keyframes` config         | `gsap.fromTo()`      | `gsap.fromTo()`       | `gsap.fromTo()`      |
| `timing.duration` (token) | `animation-duration`                      | `duration-[token]`         | `duration: 0.6`      | `duration: 0.6`       | `duration: 0.6`      |
| `timing.easing` (token)   | `animation-timing-function`               | `ease-[token]`             | `ease: "power2.out"` | `ease: "power2.out"`  | `ease: "power2.out"` |
| `stagger.tier` (token)    | `animation-delay: calc()`                 | `[animation-delay:calc()]` | `stagger: { each }`  | `stagger: { each }`   | `stagger: { each }`  |
| `trigger.type: scroll`    | `animation-timeline: scroll()`            | not supported              | `scrollTrigger: {}`  | `scrollTrigger: {}`   | `scrollTrigger: {}`  |
| `trigger.type: hover`     | `:hover` selector                         | `hover:` variant           | `addEventListener`   | `contextSafe()` event | `onMounted` event    |
| `a11y.reduced_motion`     | `@media (prefers-reduced-motion: reduce)` | `motion-reduce:`           | `gsap.matchMedia()`  | `gsap.matchMedia()`   | `gsap.matchMedia()`  |
| `sequence.position`       | N/A                                       | N/A                        | timeline `.to(pos)`  | timeline `.to(pos)`   | timeline `.to(pos)`  |
