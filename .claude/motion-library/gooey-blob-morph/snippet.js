gsap.registerPlugin(MorphSVGPlugin);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="gooey-blob-morph"]').forEach((block) => {
    const shapes = gsap.utils.toArray('[data-motion-shape]', block);
    if (shapes.length < 2) return;
    const tl = gsap.timeline({ repeat: -1, repeatDelay: 0.6 });
    for (let index = 1; index < shapes.length; index += 1) tl.to(shapes[0], { morphSVG: shapes[index], duration: 0.8, ease: 'power2.inOut' });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="gooey-blob-morph"]", { clearProps: "all" });
});
