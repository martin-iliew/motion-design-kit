gsap.registerPlugin(Draggable);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="before-after-drag-reveal"]').forEach((block) => {
    const handle = block.querySelector('[data-motion="before-after-drag-reveal"] [data-motion-handle]');
    const target = block.querySelector('[data-motion-target]');
    if (!handle || !target) return;
    const update = () => {
      const progress = gsap.utils.clamp(0, 1, (handle.offsetLeft || 0) / block.getBoundingClientRect().width);
      gsap.set(target, { transformOrigin: 'left center', scaleX: progress });
    };
    Draggable.create(handle, { type: 'x', bounds: block, inertia: true, onDrag: update, onThrowUpdate: update });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="before-after-drag-reveal"], [data-motion="before-after-drag-reveal"] [data-motion-handle], [data-motion="before-after-drag-reveal"] [data-motion-target]", { clearProps: "all" });
});
