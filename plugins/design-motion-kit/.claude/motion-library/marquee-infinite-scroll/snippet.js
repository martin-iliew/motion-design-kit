// Marquee / Infinite Scroll — GSAP-enhanced continuous loop
// Requires: gsap core (no plugins needed)

const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const marquees = gsap.utils.toArray(".marquee-track");
  marquees.forEach(track => {
    // Duplicate content for seamless loop
    track.innerHTML += track.innerHTML;
    const totalWidth = track.scrollWidth / 2;

    gsap.to(track, {
      x: -totalWidth,
      duration: totalWidth / 50,  // speed: ~50px/s
      ease: "none",               
      repeat: -1,
      modifiers: {
        x: gsap.utils.unitize(x => parseFloat(x) % totalWidth),
      },
    });
  });

  return () => gsap.killTweensOf(".marquee-track");
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".marquee-track", { clearProps: "x" });
});
