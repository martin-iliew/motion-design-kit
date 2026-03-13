gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="odometer-digit-roll"] [data-motion-item]').forEach((digit) => {
    const end = Number(digit.dataset.digit || 0);
    gsap.fromTo(digit, { yPercent: 100 }, { yPercent: -100 * end, duration: 0.8, ease: 'power2.out', scrollTrigger: { trigger: digit.closest('[data-motion="odometer-digit-roll"]'), start: 'top 85%' } });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="odometer-digit-roll"] [data-motion-item]", { clearProps: "all" });
});
