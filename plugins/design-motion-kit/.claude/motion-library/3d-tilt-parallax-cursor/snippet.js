const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll(".tilt-card, [data-tilt-card]").forEach((card) => {
    const xTo = gsap.quickTo(card, "rotationY", { duration: 0.2, ease: "power3.out" });
    const yTo = gsap.quickTo(card, "rotationX", { duration: 0.2, ease: "power3.out" });
    card.addEventListener("mouseenter", () => {
      gsap.to(card, { scale: 1.03, duration: 0.2, ease: "power2.out" });
    });
    card.addEventListener("mousemove", (event) => {
      const rect = card.getBoundingClientRect();
      const offsetX = (event.clientX - rect.left - rect.width / 2) / rect.width;
      const offsetY = (event.clientY - rect.top - rect.height / 2) / rect.height;
      xTo(offsetX * 18);
      yTo(offsetY * -18);
    });
    card.addEventListener("mouseleave", () => {
      xTo(0);
      yTo(0);
      gsap.to(card, { scale: 1, duration: 0.25, ease: "power2.out" });
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".tilt-card, [data-tilt-card]", { clearProps: "all" });
});
