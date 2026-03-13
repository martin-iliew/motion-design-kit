gsap.registerPlugin(Draggable);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="draggable-card-deck"] [data-motion-item]').forEach((item, index) => {
    gsap.set(item, { y: index * 8, rotation: (index - 1) * 2 });
    Draggable.create(item, { type: 'x,y', inertia: true, onPress() { gsap.to(item, { scale: 1.02, duration: 0.15, ease: 'power2.out' }) }, onRelease() { gsap.to(item, { scale: 1, duration: 0.2, ease: 'power2.out' }) } });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="draggable-card-deck"] [data-motion-item]", { clearProps: "all" });
});
