const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const items = gsap.utils.toArray('[data-motion="horizontal-loop-carousel"] [data-motion-item]');
  if (!items.length) return;
  const width = items.reduce((total, item) => total + item.offsetWidth, 0);
  gsap.to(items, { x: `-=${width}`, duration: 18, ease: 'none', repeat: -1, modifiers: { x: (value) => `${gsap.utils.wrap(-width, 0, parseFloat(value))}px` } });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="horizontal-loop-carousel"] [data-motion-item]", { clearProps: "all" });
});
