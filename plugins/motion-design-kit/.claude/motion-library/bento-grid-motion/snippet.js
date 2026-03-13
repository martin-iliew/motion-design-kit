gsap.registerPlugin(Flip);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const grid = document.querySelector(".bento-grid");
  if (!grid) return;
  const cards = gsap.utils.toArray(".bento-grid .bento-card");
  cards.forEach((card) => {
    card.addEventListener("click", () => {
      const state = Flip.getState(cards);
      const expanded = card.classList.contains("bento-card--expanded");
      cards.forEach((item) => item.classList.remove("bento-card--expanded"));
      if (!expanded) card.classList.add("bento-card--expanded");
      Flip.from(state, { duration: 0.45, ease: "power2.inOut", absolute: true, nested: true });
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".bento-grid .bento-card", { clearProps: "all" });
});
