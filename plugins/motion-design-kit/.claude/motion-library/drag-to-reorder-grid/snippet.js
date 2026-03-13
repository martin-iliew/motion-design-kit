gsap.registerPlugin(Draggable, Flip);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="drag-to-reorder-grid"] [data-motion-item]').forEach((item) => {
    Draggable.create(item, { type: 'x,y', onRelease() { const state = Flip.getState('[data-motion="drag-to-reorder-grid"] [data-motion-item]'); item.parentNode.appendChild(item); Flip.from(state, { duration: 0.45, ease: 'power2.inOut', absolute: true }); gsap.to(item, { x: 0, y: 0, duration: 0.2, ease: 'power2.out' }); } });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="drag-to-reorder-grid"] [data-motion-item]", { clearProps: "all" });
});
