/* Motion Spec: kinetic-headline-words */

// ─── Utility: build a scroll-triggered kinetic headline ───────────────────────
function initKineticHeadline(triggerEl) {
  // 1. Split — mask:true wraps each word in an overflow:hidden container
  //    autoSplit:true re-fires onSplit() on resize/font-load events
  const split = new SplitText(triggerEl, {
    type: "lines,words,chars",
    mask: "lines",         // clips the overflow so words slide up from below
    autoSplit: true,       // handles responsive re-splitting automatically
    aria: true,            // adds aria-label on parent, aria-hidden on children
    onSplit(self) {
      // Re-animate whenever autoSplit fires (resize, font swap)
      buildTimeline(self);
    },
  });

  let tl;

  function buildTimeline(splitInstance) {
    // Kill previous timeline before rebuilding
    if (tl) tl.kill();

    tl = gsap.timeline({
      scrollTrigger: {
        trigger: triggerEl,
        start: "top 80%",
        end: "bottom 20%",
        toggleActions: "play none none reverse",
      },
      defaults: { ease: "power3.out", duration: 0.75 },  // token: impact / token: ~base (0.75 — between fast=0.3 and base=0.6; nearest: base)
    });

    // Line stagger — each line enters as a block
    tl.from(splitInstance.lines, {
      autoAlpha: 0,
      y: 60,
      stagger: { each: 0.13, from: "start" },  // token: loose
    });

    // Word-level reveal inside each line (clip-mask effect via mask:"lines")
    // Words slide up from yPercent: 100 (fully below the mask boundary)
    tl.from(
      splitInstance.words,
      {
        yPercent: 100,
        autoAlpha: 0,
        stagger: { each: 0.05, from: "start" },  // token: tight
        duration: 0.6,                            // token: base
        ease: "power2.out",                       // token: entrance
      },
      "<0.05" // overlap with the line animation for fluidity
    );
  }

  // Initial build
  buildTimeline(split);

  // Return cleanup handle
  return () => {
    if (tl) tl.kill();
    split.revert(); // restores original DOM — critical for React/SPA cleanup
  };
}

// ─── Character-level stagger (hero display text) ──────────────────────────────
function initCharStagger(el) {
  const split = new SplitText(el, {
    type: "chars,words",
    mask: "chars",
    aria: true,
  });

  const tl = gsap.timeline({
    defaults: { ease: "power3.out", duration: 0.55 },  // token: impact / token: ~base (0.55 — between fast=0.3 and base=0.6; nearest: base)
  });

  tl.from(split.chars, {
    autoAlpha: 0,
    y: 40,
    rotationX: -90,      // perspective flip from below
    transformOrigin: "50% 100%",
    stagger: { each: 0.025, from: "start" },  // token: tight
  });

  return () => {
    tl.kill();
    split.revert();
  };
}

// ─── Accessibility wrapper — ALL animation inside matchMedia ──────────────────
const mm = gsap.matchMedia();
const cleanups = [];

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // Animate
  document.querySelectorAll("[data-kinetic]").forEach((el) => {
    cleanups.push(initKineticHeadline(el));
  });

  document.querySelectorAll("[data-kinetic-chars]").forEach((el) => {
    cleanups.push(initCharStagger(el));
  });

  // Cleanup returned from matchMedia context
  return () => {
    cleanups.forEach((fn) => fn());
    cleanups.length = 0;
  };
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // Show text immediately without animation — no SplitText needed
  gsap.set("[data-kinetic], [data-kinetic-chars]", { opacity: 1, y: 0 });
});
