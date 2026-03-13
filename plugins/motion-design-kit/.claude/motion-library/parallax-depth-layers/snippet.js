/* Motion Spec: parallax-layer-scroll */

// ── gsap.matchMedia() guards the whole animation block ──────
// Users who prefer reduced motion see NO parallax movement.
// Full motion users get the layered depth effect.
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  const scene   = document.querySelector("[data-parallax-scene]");
  const layers  = scene.querySelectorAll(".layer[data-depth]");

  // One shared ScrollTrigger drives all layers — cheaper than
  // one trigger per layer.
  const st = ScrollTrigger.create({
    trigger: scene,
    start:   "top top",
    end:     "bottom top",
    scrub:   1.5,          // lag in seconds — higher = smoother/lazier (not a token)
    onUpdate: (self) => {
      const progress = self.progress; // 0 → 1

      layers.forEach((layer) => {
        const depth     = parseFloat(layer.dataset.depth); // 0.1 – 0.75
        const maxTravel = 120;                              // px total movement
        const yOffset   = progress * maxTravel * depth;

        // translate3d keeps movement on the GPU compositor thread.
        // Avoid top/margin — those trigger layout.
        gsap.set(layer, {
          y: yOffset,
          force3D: true,   // always use 3D matrix for GPU promotion
        });
      });
    },
  });

  // Cleanup function — called when the media query stops matching
  return () => st.kill();
});

// ── Reduced-motion fallback: static scene, no movement ──────
mm.add("(prefers-reduced-motion: reduce)", () => {
  // Layers stay at y:0. No ScrollTrigger created.
  // Optionally apply a subtle CSS fade-in instead:
  document.querySelectorAll(".layer").forEach((el) => {
    el.style.opacity = "1";
  });
});
