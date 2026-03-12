gsap.registerPlugin(Flip);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="shared-element-gallery-expand"]').forEach((gallery) => {
    const expanded = gallery.querySelector('[data-motion-expanded]');
    const items = gsap.utils.toArray('[data-motion-item]', gallery);
    if (!expanded || !items.length) return;
    items.forEach((item) => item.addEventListener('click', () => {
      const state = Flip.getState([item, expanded]);
      expanded.appendChild(item);
      expanded.classList.add('is-open');
      Flip.from(state, { duration: 0.55, ease: 'power2.inOut', absolute: true });
    }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="shared-element-gallery-expand"]", { clearProps: "all" });
});
