gsap.registerPlugin(ScrambleTextPlugin);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="scramble-hover-relabel"]').forEach((node) => {
    const finalText = node.dataset.scrambleLabel || node.textContent.trim();
    const handler = () => gsap.to(node, { duration: 0.6, ease: 'none', scrambleText: { text: finalText, chars: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', speed: 0.35, revealDelay: 0.08 } });
    node.addEventListener('mouseenter', handler);
    node.addEventListener('focus', handler);
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="scramble-hover-relabel"]", { clearProps: "all" });
});
