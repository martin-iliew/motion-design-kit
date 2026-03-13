# CSS-Only Pattern Templates

4 CSS-only patterns for animations that don't need GSAP. Use these when the pattern is purely visual (no scroll trigger, no interaction state beyond hover). Every pattern includes a `prefers-reduced-motion` guard.

---

## Morphing Button States

Use for primary buttons that shift shape and depth on hover/active. No JS needed.

```css
.btn {
  --btn-bg: #3b82f6;
  background: var(--btn-bg);
  border-radius: 0.5rem;
  transition: background 0.3s cubic-bezier(0.0, 0.0, 0.2, 1),       /* fast / entrance */
              border-radius 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),  /* fast / spring */
              transform 0.15s cubic-bezier(0.0, 0.0, 0.2, 1);        /* micro / entrance */
}
.btn:hover {
  --btn-bg: #2563eb;
  border-radius: 1.5rem;
  transform: translateY(-2px);
}
.btn:active {
  transform: scale(0.96) translateY(0);
}
@media (prefers-reduced-motion: reduce) {
  .btn { transition: none; }
}
```

---

## Idle Breathing Pulse

Use for CTAs, badges, or notification dots that pulse gently to draw attention. Continuous animation — no trigger needed.

```css
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.9; }
  50% { transform: scale(1.04); opacity: 1; }
}
.cta-pulse {
  animation: breathe 3s ease-in-out infinite; /* slow, continuous */
}
@media (prefers-reduced-motion: reduce) {
  .cta-pulse { animation: none; opacity: 1; transform: none; }
}
```

---

## Gradient Text Flow

Use for hero headings or brand text with a shifting gradient background. Pure CSS, no JS.

```css
.gradient-text {
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #3b82f6);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-shift 6s ease-in-out infinite;
}
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@media (prefers-reduced-motion: reduce) {
  .gradient-text {
    animation: none;
    background-position: 0% 50%;
  }
}
```

---

## Variable Font Morphing

Use for headings that shift weight/width on hover or when scrolled into view. Requires a variable font (e.g., Inter, Work Sans, Outfit).

```css
.morph-heading {
  font-variation-settings: "wght" 400, "wdth" 100;
  transition: font-variation-settings 0.6s cubic-bezier(0.0, 0.0, 0.2, 1); /* base / entrance */
}
.morph-heading:hover,
.morph-heading.in-view {
  font-variation-settings: "wght" 800, "wdth" 110;
}
@media (prefers-reduced-motion: reduce) {
  .morph-heading { transition: none; }
}
```

To trigger `.in-view` on scroll without GSAP, use IntersectionObserver:

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => e.target.classList.toggle("in-view", e.isIntersecting));
}, { threshold: 0.3 });
document.querySelectorAll(".morph-heading").forEach(el => observer.observe(el));
```
