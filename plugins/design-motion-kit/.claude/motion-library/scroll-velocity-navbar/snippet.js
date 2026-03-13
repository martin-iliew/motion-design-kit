gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const nav = document.querySelector('[data-motion="scroll-velocity-navbar"]');
  if (!nav) return;
  ScrollTrigger.create({
    start: 'top top',
    end: 'bottom bottom',
    onUpdate: (self) => {
      const velocity = self.getVelocity();
      if (self.direction === 1 && velocity > 180) gsap.to(nav, { yPercent: -100, duration: 0.3, ease: 'power2.in', overwrite: true });
      if (self.direction === -1 || velocity < -180) gsap.to(nav, { yPercent: 0, duration: 0.3, ease: 'power2.out', overwrite: true });
    },
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="scroll-velocity-navbar"]", { clearProps: "all" });
});
