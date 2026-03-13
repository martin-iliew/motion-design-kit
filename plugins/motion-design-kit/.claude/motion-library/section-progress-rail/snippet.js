gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const root = document.querySelector('[data-motion="section-progress-rail"]');
  const target = document.querySelector('[data-motion="section-progress-rail"] [data-motion-target]') || root.querySelector('[data-motion-rail]');
  if (!root || !target) return;
  gsap.set(target, { transformOrigin: 'top center', scaleY: 0 });
  gsap.to(target, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: root, start: 'top center', end: 'bottom center', scrub: true } });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="section-progress-rail"], [data-motion="section-progress-rail"] [data-motion-target]", { clearProps: "all" });
});
