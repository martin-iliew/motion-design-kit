gsap.registerPlugin(SplitText, ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.utils.toArray('[data-motion="splittext-char-rotation-burst"]').forEach((block) => {
    const split = new SplitText(block, { type: 'chars', aria: true });
    gsap.from(split.chars, { rotationX: -80, yPercent: 110, autoAlpha: 0, transformOrigin: '50% 100%', duration: 0.7, ease: 'power3.out', stagger: { each: 0.025, from: 'center' }, scrollTrigger: { trigger: block, start: 'top 85%' }, onComplete: () => split.revert() });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="splittext-char-rotation-burst"]", { clearProps: "all" });
});
