gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll("[data-word-reveal]").forEach((element) => {
    const words = element.textContent.trim().split(/\s+/);
    element.innerHTML = words.map((word) => `<span class="word-reveal" style="display:inline-block;margin-right:0.25em">${word}</span>`).join("");
    gsap.from(element.querySelectorAll(".word-reveal"), {
      autoAlpha: 0,
      y: 12,
      duration: 0.7,
      ease: "power2.out",
      stagger: 0.09,
      scrollTrigger: { trigger: element, start: "top 85%", once: true },
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-word-reveal]", { clearProps: "all" });
});
