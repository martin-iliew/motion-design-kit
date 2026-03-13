const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="checkmark-success-morph"]').forEach((button) => {
    const lines = gsap.utils.toArray('[data-motion-line]', button);
    if (lines.length < 2) return;
    button.addEventListener('click', () => {
      const active = button.classList.toggle('is-active');
      gsap.to(lines[0], { y: active ? 6 : 0, rotation: active ? 45 : 0, duration: 0.3, ease: 'power2.out' });
      gsap.to(lines[1], { autoAlpha: active ? 0 : 1, scaleX: active ? 0.6 : 1, duration: 0.2, ease: 'power2.out' });
      gsap.to(lines[2] || lines[1], { y: active ? -6 : 0, rotation: active ? -45 : 0, duration: 0.3, ease: 'power2.out' });
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="checkmark-success-morph"], [data-motion="checkmark-success-morph"] [data-motion-line]", { clearProps: "all" });
});
