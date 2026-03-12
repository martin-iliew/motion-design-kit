const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="stacked-testimonial-rotator"]').forEach((stack) => {
    const items = gsap.utils.toArray('[data-motion-item]', stack);
    const layout = () => items.forEach((item, index) => gsap.to(item, { y: index * 12, scale: 1 - index * 0.04, duration: 0.25, ease: 'power2.out' }));
    layout();
    stack.querySelector('[data-motion-next]')?.addEventListener('click', () => { items.push(items.shift()); layout(); });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="stacked-testimonial-rotator"]", { clearProps: "all" });
});
