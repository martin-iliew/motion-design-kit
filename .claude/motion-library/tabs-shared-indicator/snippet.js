gsap.registerPlugin(Flip);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="tabs-shared-indicator"]').forEach((group) => {
    const indicator = group.querySelector('[data-motion-indicator]');
    const items = gsap.utils.toArray('[data-motion-item]', group);
    if (!indicator || !items.length) return;
    items.forEach((item) => item.addEventListener('click', () => {
      const state = Flip.getState(indicator);
      item.appendChild(indicator);
      Flip.from(state, { duration: 0.45, ease: 'power2.inOut', absolute: true });
    }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="tabs-shared-indicator"]", { clearProps: "all" });
});
