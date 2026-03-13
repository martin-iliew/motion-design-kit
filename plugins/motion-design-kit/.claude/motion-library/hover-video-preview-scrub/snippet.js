const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll('[data-motion="hover-video-preview-scrub"]').forEach((card) => {
    const video = card.querySelector('video');
    if (!video) return;
    const state = { progress: 0 };
    const update = () => video.duration && (video.currentTime = state.progress * video.duration);
    card.addEventListener('mouseenter', () => gsap.to(state, { progress: 1, duration: 0.9, ease: 'power2.out', onUpdate: update }));
    card.addEventListener('mouseleave', () => gsap.to(state, { progress: 0, duration: 0.45, ease: 'power2.out', onUpdate: update }));
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-motion="hover-video-preview-scrub"]", { clearProps: "all" });
});
