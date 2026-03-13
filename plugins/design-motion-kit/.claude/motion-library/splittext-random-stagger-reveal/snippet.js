gsap.registerPlugin(SplitText, ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.utils.toArray('[data-motion="splittext-random-stagger-reveal"]').forEach((block) => {
    const split = new SplitText(block, { type: 'words,chars', aria: true });
    const parts = split.chars.length ? split.chars : split.words;
    gsap.from(parts, { yPercent: 100, autoAlpha: 0, duration: 0.55, ease: 'power2.out', stagger: { each: 0.03, from: 'random' }, scrollTrigger: { trigger: block, start: 'top 88%' }, onComplete: () => split.revert() });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="splittext-random-stagger-reveal"]", { clearProps: "all" });
});
