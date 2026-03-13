gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const root = document.querySelector('[data-motion="3d-cylinder-text-scroll"]');
  const target = document.querySelector('[data-motion="3d-cylinder-text-scroll"] [data-motion-target]') || root;
  if (!root || !target) return;
  gsap.fromTo(target, { autoAlpha: 1, yPercent: 10, scale: 1.05 }, {
    autoAlpha: 1,
    yPercent: -8,
    scale: 0.96,
    ease: 'none',
    scrollTrigger: { trigger: root, start: 'top 85%', end: 'bottom 15%', scrub: true },
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="3d-cylinder-text-scroll"], [data-motion="3d-cylinder-text-scroll"] [data-motion-target]", { clearProps: "all" });
});
