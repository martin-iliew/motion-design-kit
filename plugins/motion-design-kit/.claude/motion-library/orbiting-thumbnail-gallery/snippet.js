gsap.registerPlugin(MotionPathPlugin);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="orbiting-thumbnail-gallery"]').forEach((block) => {
    const target = block.querySelector('[data-motion-target]');
    const path = block.querySelector('[data-motion-path]');
    if (!target || !path) return;
    gsap.to(target, { duration: 8, repeat: -1, ease: 'none', motionPath: { path, align: path, autoRotate: false, alignOrigin: [0.5, 0.5] } });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="orbiting-thumbnail-gallery"], [data-motion="orbiting-thumbnail-gallery"] [data-motion-path], [data-motion="orbiting-thumbnail-gallery"] [data-motion-target]", { clearProps: "all" });
});
