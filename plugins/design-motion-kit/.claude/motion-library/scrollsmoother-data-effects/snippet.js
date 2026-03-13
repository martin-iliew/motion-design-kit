gsap.registerPlugin(ScrollTrigger, ScrollSmoother);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  if (!document.querySelector('#smooth-wrapper') || !document.querySelector('#smooth-content')) return;
  const smoother = ScrollSmoother.create({ wrapper: '#smooth-wrapper', content: '#smooth-content', smooth: 1.1, effects: true, normalizeScroll: true });
  return () => smoother.kill();
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("#smooth-wrapper, #smooth-content", { clearProps: "all" });
});
