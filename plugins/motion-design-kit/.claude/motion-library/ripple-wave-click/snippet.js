const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-ripple], button, a, .ripple-trigger");
    if (!target) return;
    const rect = target.getBoundingClientRect();
    const ripple = document.createElement("span");
    ripple.style.position = "absolute";
    ripple.style.left = `${event.clientX - rect.left}px`;
    ripple.style.top = `${event.clientY - rect.top}px`;
    ripple.style.width = "12px";
    ripple.style.height = "12px";
    ripple.style.borderRadius = "999px";
    ripple.style.background = "currentColor";
    ripple.style.opacity = "0.22";
    ripple.style.pointerEvents = "none";
    ripple.style.transform = "translate(-50%, -50%) scale(0)";
    if (getComputedStyle(target).position === "static") target.style.position = "relative";
    if (getComputedStyle(target).overflow !== "hidden") target.style.overflow = "hidden";
    target.appendChild(ripple);
    gsap.to(ripple, {
      scale: 18,
      autoAlpha: 0,
      duration: 0.55,
      ease: "power2.out",
      onComplete: () => ripple.remove(),
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {});
