const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-swipe-card], .card").forEach((card) => {
    let startX = 0;
    card.addEventListener("pointerdown", (event) => {
      startX = event.clientX;
      card.setPointerCapture?.(event.pointerId);
    });
    card.addEventListener("pointermove", (event) => {
      if (!startX) return;
      const deltaX = event.clientX - startX;
      gsap.to(card, { x: deltaX, rotation: deltaX * 0.03, duration: 0, overwrite: true });
    });
    const reset = () => {
      startX = 0;
      gsap.to(card, { x: 0, rotation: 0, duration: 0.25, ease: "power2.out" });
    };
    card.addEventListener("pointerup", reset);
    card.addEventListener("pointercancel", reset);
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-swipe-card], .card", { clearProps: "all" });
});
