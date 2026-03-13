const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="accordion-scale-reveal"]').forEach((item) => {
    const panel = item.querySelector('[data-motion-panel]');
    if (!panel) return;
    gsap.set(panel, { transformOrigin: 'top center', scaleY: 0.92, autoAlpha: 0 });
    item.addEventListener('click', () => {
      const open = item.classList.toggle('is-open');
      gsap.to(panel, { scaleY: open ? 1 : 0.92, autoAlpha: open ? 1 : 0, duration: 0.3, ease: open ? 'power2.out' : 'power2.in', overwrite: true });
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="accordion-scale-reveal"]", { clearProps: "all" });
});
