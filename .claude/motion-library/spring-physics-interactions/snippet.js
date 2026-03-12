/* Motion Spec: spring-physics-interactions */

// Register any plugins used alongside spring interactions
gsap.registerPlugin();

// ─── Accessibility guard (required) ──────────────────────────────────────────
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {

  // ── 1. Button press — back.out for tactile click feedback ─────────────────
  const buttons = document.querySelectorAll(".btn-spring");

  buttons.forEach((btn) => {
    btn.addEventListener("mousedown", () => {
      gsap.to(btn, { scale: 0.92, duration: 0.12, ease: "power2.in" });  
    });

    btn.addEventListener("mouseup", () => {
      gsap.to(btn, { scale: 1, duration: 0.5, ease: "back.out(2.5)" }); 
    });

    btn.addEventListener("keyup", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        gsap.fromTo(btn, { scale: 0.92 }, { scale: 1, duration: 0.5, ease: "back.out(2.5)" });  
      }
    });
  });

  // ── 2. Modal entrance — elastic.out for expressive pop-in ─────────────────
  function openModal(modal) {
    gsap.fromTo(
      modal,
      { autoAlpha: 0, scale: 0.75, y: 24 },
      { autoAlpha: 1, scale: 1, y: 0, duration: 0.65, ease: "elastic.out(1, 0.4)", clearProps: "scale,y" }  
    );
  }

  function closeModal(modal) {
    gsap.to(modal, { autoAlpha: 0, scale: 0.9, y: 12, duration: 0.22, ease: "power3.in" }); 
  }

  // ── 3. Icon / badge spring-in ─────────────────────────────────────────────
  function springInIcon(icon) {
    gsap.fromTo(
      icon,
      { scale: 0, rotation: -15 },
      { scale: 1, rotation: 0, duration: 0.7, ease: "elastic.out(1, 0.3)", clearProps: "scale,rotation" }  
    );
  }

  // ── 4. Card hover lift — back.out for subtle depth feel ───────────────────
  const cards = document.querySelectorAll(".card-spring");

  cards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      gsap.to(card, { y: -6, scale: 1.02, duration: 0.45, ease: "back.out(1.7)" });  
    });
    card.addEventListener("mouseleave", () => {
      gsap.to(card, { y: 0, scale: 1, duration: 0.35, ease: "power2.out" }); 
    });
  });

  // ── 5. Staggered list spring-in ───────────────────────────────────────────
  gsap.from(".list-item", {
    autoAlpha: 0, scale: 0.85, y: 20,
    duration: 0.6,                              
    ease: "back.out(1.7)",                     
    stagger: { each: 0.09, from: "start" },     
  });

  return () => {
    gsap.killTweensOf(".btn-spring, .card-spring, .list-item");
  };
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".btn-spring, .card-spring, .list-item", { clearProps: "all" });
});
