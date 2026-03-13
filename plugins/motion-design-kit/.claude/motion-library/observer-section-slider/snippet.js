gsap.registerPlugin(Observer);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const root = document.querySelector('[data-motion="observer-section-slider"]');
  if (!root) return;
  const sections = gsap.utils.toArray('[data-motion="observer-section-slider"] [data-motion-item]');
  if (sections.length < 2) return;
  let index = 0;
  gsap.set(sections, { autoAlpha: 0, yPercent: 10 });
  gsap.set(sections[0], { autoAlpha: 1, yPercent: 0 });
  const gotoSection = (next) => {
    if (next < 0 || next >= sections.length || next === index) return;
    gsap.timeline().to(sections[index], { autoAlpha: 0, yPercent: -8, duration: 0.35, ease: 'power2.out' }).fromTo(sections[next], { autoAlpha: 0, yPercent: 8 }, { autoAlpha: 1, yPercent: 0, duration: 0.45, ease: 'power2.out' }, '<');
    index = next;
  };
  Observer.create({ target: root, type: 'wheel,touch,pointer', tolerance: 12, preventDefault: true, onUp: () => gotoSection(index + 1), onDown: () => gotoSection(index - 1) });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="observer-section-slider"], [data-motion="observer-section-slider"] [data-motion-item]", { clearProps: "all" });
});
