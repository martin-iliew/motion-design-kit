/* Motion Spec: flip-grid-reorder */

// ─── Accessible motion guard (required pattern) ────────────────────────────
const mm = gsap.matchMedia();

mm.add(
  {
    motion: "(prefers-reduced-motion: no-preference)",
    reduced: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    const { motion } = context.conditions;

    // ─── Grid filter / layout reflow example ─────────────────────────────
    const grid = document.querySelector(".card-grid");
    const filterButtons = document.querySelectorAll("[data-filter]");

    filterButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const filter = btn.dataset.filter;

        if (motion) {
          // STEP 1 — FIRST: capture current positions of all grid cards
          const state = Flip.getState(".card", {
            props: "opacity",   // also capture opacity so fades are included
          });

          // STEP 2 — LAST: apply the DOM/class change
          grid.querySelectorAll(".card").forEach((card) => {
            const matches = filter === "all" || card.dataset.category === filter;
            card.classList.toggle("hidden", !matches);
          });

          // STEP 3 & 4 — INVERT + PLAY: animate from recorded state
          Flip.from(state, {
            duration: 0.55,          // token: fast
            ease: "power2.inOut",    // token: transition
            stagger: 0.05,           // token: tight
            absolute: true,       // prevents siblings snapping mid-animation
            prune: true,          // skip elements whose position hasn't changed
            onEnter: (elements) =>
              gsap.fromTo(
                elements,
                { opacity: 0, scale: 0.85 },
                { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.4)" }
                //                             ^^^^^^^^^^^  token: fast
                //                                          ^^^^^^^^^^^^^^^^  token: spring (amplitude tuned to 1.4)
              ),
            onLeave: (elements) =>
              gsap.to(elements, {
                opacity: 0,
                scale: 0.85,
                duration: 0.3,      // token: fast
                ease: "power2.in",  // token: exit
              }),
          });
        } else {
          // Reduced motion: instant state change, no animation
          grid.querySelectorAll(".card").forEach((card) => {
            const matches = filter === "all" || card.dataset.category === filter;
            card.classList.toggle("hidden", !matches);
          });
        }
      });
    });

    // ─── Shared-element card-to-detail expansion ─────────────────────────
    document.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("click", () => {
        if (!motion) return;

        // Assign a stable flip ID so Flip can match card → detail panel
        card.dataset.flipId = "active-card";
        const detail = document.querySelector(".detail-panel");
        detail.dataset.flipId = "active-card";

        const state = Flip.getState([card, detail]);

        card.classList.add("is-hidden");
        detail.classList.add("is-visible");

        Flip.from(state, {
          duration: 0.65,          // token: base
          ease: "power2.inOut",    // token: transition
          nested: true,           // card contains animated children
          zIndex: 100,            // keep expanding card above siblings
        });
      });
    });

    // Return cleanup — Flip timelines created inside matchMedia are
    // automatically killed when the media condition no longer matches
    return () => {
      Flip.killFlipsOf("*");
    };
  }
);
