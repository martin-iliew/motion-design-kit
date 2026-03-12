const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="form-focus-cascade"]').forEach((form) => {
    const fields = gsap.utils.toArray('[data-motion-item]', form);
    fields.forEach((field, index) => {
      field.addEventListener('focusin', () => gsap.to(fields.slice(index), { y: -2, duration: 0.18, ease: 'power2.out', stagger: 0.02 }));
      field.addEventListener('focusout', () => gsap.to(fields, { y: 0, duration: 0.18, ease: 'power2.out', overwrite: true }));
    });
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="form-focus-cascade"]", { clearProps: "all" });
});
