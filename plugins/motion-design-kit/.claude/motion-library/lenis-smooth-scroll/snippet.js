const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const lenis = new Lenis({
    duration: 1.2,
    easing: (value) => Math.min(1, 1.001 - Math.pow(2, -10 * value)),
    orientation: "vertical",
    smoothWheel: true,
  });

  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);

  return () => {
    lenis.destroy();
  };
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  ScrollTrigger.update();
});
    