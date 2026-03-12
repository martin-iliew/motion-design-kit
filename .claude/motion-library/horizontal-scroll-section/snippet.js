// Horizontal Scroll Section — ScrollTrigger pin + horizontal scrub
// Requires: gsap + ScrollTrigger

gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const container = document.querySelector(".horizontal-section");
  const track = container.querySelector(".horizontal-track");

  gsap.to(track, {
    x: () => -(track.scrollWidth - container.offsetWidth),
    ease: "none",   // token: scrub
    scrollTrigger: {
      trigger: container,
      pin: true,
      scrub: 0.5,
      start: "top top",
      end: () => "+=" + (track.scrollWidth - container.offsetWidth),
      invalidateOnRefresh: true,
    },
  });

  return () => ScrollTrigger.getAll().forEach(t => t.kill());
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".horizontal-track", { clearProps: "x" });
  gsap.set(".horizontal-track > *", { autoAlpha: 1 });
});
