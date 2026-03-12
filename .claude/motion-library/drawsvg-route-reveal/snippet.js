gsap.registerPlugin(DrawSVGPlugin, ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="drawsvg-route-reveal"]').forEach((block) => {
    const path = block.querySelector('[data-motion-path]') || block.querySelector('path');
    if (!path) return;
    gsap.from(path, { drawSVG: '0%', duration: 0.8, ease: 'power2.out', scrollTrigger: { trigger: block, start: 'top 85%' } });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="drawsvg-route-reveal"], [data-motion="drawsvg-route-reveal"] [data-motion-path]", { clearProps: "all" });
});
