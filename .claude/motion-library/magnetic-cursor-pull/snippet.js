/* Motion Spec: magnetic-cursor-pull */

(function initMagneticButtons() {
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    const buttons = document.querySelectorAll(".mag-btn");

    buttons.forEach((btn) => {
      const inner = btn.querySelector(".mag-btn__inner");
      const strength = parseFloat(btn.dataset.strength ?? "0.4");
      const maxDist = parseFloat(btn.dataset.distance ?? "80");

      function onMove(e) {
        const rect = btn.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const dx = e.clientX - centerX;
        const dy = e.clientY - centerY;

        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > maxDist) return;

        gsap.to(btn, {
          x: dx * strength,
          y: dy * strength,
          duration: 0.4,
          ease: "power3.out",
          overwrite: "auto",
        });

        if (inner) {
          gsap.to(inner, {
            x: dx * strength * 0.5,
            y: dy * strength * 0.5,
            duration: 0.4,
            ease: "power3.out",
            overwrite: "auto",
          });
        }
      }

      function onLeave() {
        gsap.to(btn, {
          x: 0,
          y: 0,
          duration: 0.7,
          ease: "elastic.out(1, 0.4)",
          overwrite: "auto",
        });

        if (inner) {
          gsap.to(inner, {
            x: 0,
            y: 0,
            duration: 0.7,
            ease: "elastic.out(1, 0.4)",
            overwrite: "auto",
          });
        }
      }

      btn.addEventListener("mousemove", onMove);
      btn.addEventListener("mouseleave", onLeave);

      return () => {
        btn.removeEventListener("mousemove", onMove);
        btn.removeEventListener("mouseleave", onLeave);
        gsap.set([btn, inner].filter(Boolean), { x: 0, y: 0 });
      };
    });
  });

  mm.add("(prefers-reduced-motion: reduce)", () => {
    // No animation; elements remain stationary.
  });
})();
