gsap.registerPlugin(SplitText, ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.utils.toArray('[data-motion="splittext-line-mask-lift"]').forEach((block) => {
    const split = new SplitText(block, { type: 'lines', mask: 'lines', autoSplit: true, aria: true });
    gsap.from(split.lines, { yPercent: 110, autoAlpha: 0, duration: 0.85, ease: 'power3.out', stagger: 0.08, scrollTrigger: { trigger: block, start: 'top 85%' }, onComplete: () => split.revert() });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="splittext-line-mask-lift"]", { clearProps: "all" });
});
