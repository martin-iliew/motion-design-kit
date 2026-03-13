gsap.registerPlugin(ScrambleTextPlugin);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-scramble-text]").forEach((element) => {
    const finalText = element.dataset.scrambleText || element.textContent.trim();
    gsap.to(element, {
      duration: 1.1,
      ease: "none",
      scrambleText: {
        text: finalText,
        chars: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*",
        speed: 0.35,
        revealDelay: 0.1,
      },
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  document.querySelectorAll("[data-scramble-text]").forEach((element) => {
    element.textContent = element.dataset.scrambleText || element.textContent.trim();
  });
});
