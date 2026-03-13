const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const preview = document.querySelector('[data-motion="cursor-image-preview-trail"] [data-motion-target]');
  if (!preview) return;
  const xTo = gsap.quickTo(preview, 'x', { duration: 0.2, ease: 'power3.out' });
  const yTo = gsap.quickTo(preview, 'y', { duration: 0.2, ease: 'power3.out' });
  document.querySelectorAll('[data-motion="cursor-image-preview-trail"] [data-motion-item]').forEach((item) => {
    item.addEventListener('mouseenter', () => gsap.to(preview, { autoAlpha: 1, scale: 1, duration: 0.18, ease: 'power2.out' }));
    item.addEventListener('mousemove', (event) => { xTo(event.clientX + 18); yTo(event.clientY + 18); });
    item.addEventListener('mouseleave', () => gsap.to(preview, { autoAlpha: 0, scale: 0.96, duration: 0.16, ease: 'power2.out' }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="cursor-image-preview-trail"] [data-motion-item], [data-motion="cursor-image-preview-trail"] [data-motion-target]", { clearProps: "all" });
});
