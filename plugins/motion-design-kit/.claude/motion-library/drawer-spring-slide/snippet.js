gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="drawer-spring-slide"]').forEach((block) => {
    const target = block.querySelector('[data-motion-target]') || block;
    gsap.fromTo(target, { autoAlpha: 0, y: 20, scale: 0.98 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.35, ease: 'power2.out', stagger: 0.05, scrollTrigger: { trigger: block, start: 'top 85%' } });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="drawer-spring-slide"], [data-motion="drawer-spring-slide"] [data-motion-target]", { clearProps: "all" });
});
