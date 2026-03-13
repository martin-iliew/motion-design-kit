const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="tooltip-follow-reveal"]').forEach((trigger) => {
    const bubble = trigger.querySelector('[data-motion-bubble]');
    if (!bubble) return;
    const xTo = gsap.quickTo(bubble, 'x', { duration: 0.18, ease: 'power3.out' });
    const yTo = gsap.quickTo(bubble, 'y', { duration: 0.18, ease: 'power3.out' });
    trigger.addEventListener('mouseenter', () => gsap.to(bubble, { autoAlpha: 1, scale: 1, duration: 0.18, ease: 'power2.out' }));
    trigger.addEventListener('mousemove', (event) => {
      const rect = trigger.getBoundingClientRect();
      xTo(event.clientX - rect.left - rect.width / 2);
      yTo(event.clientY - rect.top - rect.height / 2 - 16);
    });
    trigger.addEventListener('mouseleave', () => gsap.to(bubble, { autoAlpha: 0, scale: 0.96, duration: 0.14, ease: 'power2.out' }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="tooltip-follow-reveal"], [data-motion="tooltip-follow-reveal"] [data-motion-bubble]", { clearProps: "all" });
});
