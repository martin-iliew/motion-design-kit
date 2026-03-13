const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="radial-icon-burst"]').forEach((button) => {
    const items = gsap.utils.toArray('[data-motion-item]', button);
    button.addEventListener('click', () => items.forEach((item, index) => {
      const angle = (Math.PI * 2 * index) / Math.max(items.length, 1);
      gsap.fromTo(item, { x: 0, y: 0, scale: 0.4, autoAlpha: 1 }, { x: Math.cos(angle) * 32, y: Math.sin(angle) * 32, scale: 1, autoAlpha: 0, duration: 0.45, ease: 'power2.out' });
    }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="radial-icon-burst"]", { clearProps: "all" });
});
