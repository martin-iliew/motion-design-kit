const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const canvas = document.getElementById("particle-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const particles = Array.from({ length: 40 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    r: 1 + Math.random() * 2,
    o: 0.04 + Math.random() * 0.12,
  }));

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };
  resize();
  window.addEventListener("resize", resize, { passive: true });

  particles.forEach((particle) => {
    gsap.to(particle, {
      x: () => Math.random() * window.innerWidth,
      y: () => Math.random() * window.innerHeight,
      o: () => 0.04 + Math.random() * 0.12,
      duration: () => 18 + Math.random() * 20,
      ease: "none",
      repeat: -1,
      yoyo: true,
    });
  });

  gsap.ticker.add(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((particle) => {
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(160,170,220,${particle.o})`;
      ctx.fill();
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {});
