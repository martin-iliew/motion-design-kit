const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="toast-stack-dismiss"] [data-motion-item]').forEach((item, index) => {
    gsap.set(item, { y: index * 10, scale: 1 - index * 0.04 });
    const dismiss = item.querySelector('[data-toast-dismiss]');
    if (!dismiss) return;
    dismiss.addEventListener('click', () => gsap.to(item, { x: 64, autoAlpha: 0, duration: 0.25, ease: 'power2.in', onComplete: () => item.remove() }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="toast-stack-dismiss"] [data-motion-item]", { clearProps: "all" });
});
