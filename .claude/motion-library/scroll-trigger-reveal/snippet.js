/* Motion Spec: scroll-trigger-reveal */

// Always register before use
gsap.registerPlugin(ScrollTrigger);

// ─── Accessibility guard (required) ───────────────────────────────────────
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // ── 1. Single element reveal ─────────────────────────────────────────
  gsap.from(".hero-heading", {
    scrollTrigger: {
      trigger: ".hero-heading",
      start: "top 85%",         // fires when top of element hits 85% down the viewport
      toggleActions: "play none none reverse",
    },
    autoAlpha: 0,
    y: 48,
    duration: 0.9,              // token: ~slow (0.9 — between base=0.6 and slow=1.0; nearest: slow)
    ease: "power3.out",         // token: impact
  });

  // ── 2. Staggered card grid reveal ────────────────────────────────────
  gsap.from(".card", {
    scrollTrigger: {
      trigger: ".card-grid",
      start: "top 80%",
      toggleActions: "play none none none",
    },
    autoAlpha: 0,
    y: 40,
    duration: 0.6,              // token: base
    stagger: 0.09,              // token: medium
    ease: "power2.out",         // token: entrance
  });

  // ── 3. Batch reveal — performance-optimized for many elements ────────
  ScrollTrigger.batch(".list-item", {
    start: "top 88%",
    onEnter: (elements) =>
      gsap.from(elements, {
        autoAlpha: 0,
        y: 30,
        stagger: 0.09,          // token: medium
        duration: 0.55,         // token: ~base (0.55 — between fast=0.3 and base=0.6; nearest: base)
        ease: "power2.out",     // token: entrance
      }),
    onLeaveBack: (elements) =>
      gsap.set(elements, { autoAlpha: 0, y: 30, clearProps: false }),
  });

  // ── 4. Scrubbed section — ties animation to scroll position ──────────
  const scrubbedTl = gsap.timeline({
    scrollTrigger: {
      trigger: ".feature-section",
      pin: true,
      start: "top top",
      end: "+=600",
      scrub: 1,                 // 1s lag for smooth catch-up
      invalidateOnRefresh: true,
    },
  });
  scrubbedTl
    .from(".feature-img", { autoAlpha: 0, scale: 0.92, ease: "none" })
    .from(".feature-text", { autoAlpha: 0, x: 60, ease: "none" }, "<0.2");

  // ── 5. Lenis smooth-scroll integration ───────────────────────────────
  // Uncomment if using Lenis in your project:
  // const lenis = new Lenis({ lerp: 0.08, wheelMultiplier: 1.4 });
  // lenis.on("scroll", ScrollTrigger.update);
  // gsap.ticker.add((time) => lenis.raf(time * 1000));
  // gsap.ticker.lagSmoothing(0);

  // Cleanup function — called when matchMedia condition no longer matches
  return () => {
    ScrollTrigger.getAll().forEach((t) => t.kill());
  };
});

// Reduced-motion fallback — ensure elements are visible without animation
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(
    [".hero-heading", ".card", ".list-item", ".feature-img", ".feature-text"],
    { opacity: 1, clearProps: "transform" }
  );
});

// ─── React / Next.js usage pattern ────────────────────────────────────────
// useLayoutEffect(() => {
//   const ctx = gsap.context(() => {
//     // paste mm.add blocks here, scoped to containerRef
//   }, containerRef);
//   return () => ctx.revert();
// }, []);
