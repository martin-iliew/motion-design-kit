gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-counter]").forEach((element) => {
    const value = Number(element.getAttribute("data-counter") || 0);
    const state = { value: Number(element.getAttribute("data-start") || 0) };
    const render = () => {
      element.textContent = Math.round(state.value).toLocaleString();
    };
    render();
    gsap.to(state, {
      value,
      duration: Number(element.getAttribute("data-duration") || 1.6),
      ease: element.getAttribute("data-easing") || "power2.out",
      scrollTrigger: { trigger: element, start: "top 85%", once: true },
      onUpdate: render,
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {});
