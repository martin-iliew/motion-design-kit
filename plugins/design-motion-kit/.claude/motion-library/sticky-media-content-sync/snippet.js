gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const root = document.querySelector('[data-motion="sticky-media-content-sync"]');
  if (!root) return;
  const items = gsap.utils.toArray('[data-motion="sticky-media-content-sync"] [data-motion-item]');
  if (!items.length) return;
  const tl = gsap.timeline({ scrollTrigger: { trigger: root, start: 'top top', end: () => '+=' + root.offsetHeight * Math.max(items.length, 2), scrub: 0.85, pin: true } });
  items.forEach((item, index) => {
    tl.fromTo(item, { autoAlpha: index === 0 ? 1 : 0, y: 56, scale: 0.96 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.55, ease: 'power3.out' }, index === 0 ? 0 : '<0.2');
    if (index > 0) tl.to(items[index - 1], { autoAlpha: 0.25, scale: 0.96, duration: 0.3, ease: 'power2.out' }, '<');
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="sticky-media-content-sync"], [data-motion="sticky-media-content-sync"] [data-motion-item]", { clearProps: "all" });
});
