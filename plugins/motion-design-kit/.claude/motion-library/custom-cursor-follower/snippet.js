/* Motion Spec: custom-cursor-follower */

(function initCursor() {
  const dot  = document.querySelector('.c-cursor--dot');
  const ring = document.querySelector('.c-cursor--ring');

  if (!dot || !ring) return;

  const mm = gsap.matchMedia();

  mm.add(
    {
      isMouseDevice: '(hover: hover) and (pointer: fine)',
      reducedMotion: '(prefers-reduced-motion: reduce)',
    },
    (context) => {
      const { isMouseDevice, reducedMotion } = context.conditions;

      if (!isMouseDevice || reducedMotion) {
        gsap.set([dot, ring], { autoAlpha: 0 });
        document.documentElement.style.cursor = '';
        return;
      }

      const dotXTo  = gsap.quickTo(dot,  'x', { duration: 0.15, ease: 'power3.out' });
      const dotYTo  = gsap.quickTo(dot,  'y', { duration: 0.15, ease: 'power3.out' });
      const ringXTo = gsap.quickTo(ring, 'x', { duration: 0.5,  ease: 'power3.out' });
      const ringYTo = gsap.quickTo(ring, 'y', { duration: 0.5,  ease: 'power3.out' });

      gsap.set([dot, ring], { autoAlpha: 1 });

      function onMouseMove(e) {
        dotXTo(e.clientX);
        dotYTo(e.clientY);
        ringXTo(e.clientX);
        ringYTo(e.clientY);
      }

      window.addEventListener('mousemove', onMouseMove, { passive: true });

      document.addEventListener('mouseleave', () => {
        gsap.to([dot, ring], { autoAlpha: 0, duration: 0.3 });
      });
      document.addEventListener('mouseenter', () => {
        gsap.to([dot, ring], { autoAlpha: 1, duration: 0.3 });
      });

      const interactiveEls = document.querySelectorAll('a, button, [data-cursor]');

      interactiveEls.forEach((el) => {
        el.addEventListener('mouseenter', () => {
          const cursorType = el.dataset.cursor;
          ring.classList.add('is-hovering');
          if (cursorType === 'link' || el.tagName === 'A') {
            ring.classList.add('is-hovering-link');
          }
          gsap.to(dot, { scale: 0.5, duration: 0.2, ease: 'power2.out' });
        });

        el.addEventListener('mouseleave', () => {
          ring.classList.remove('is-hovering', 'is-hovering-link');
          gsap.to(dot, { scale: 1, duration: 0.3, ease: 'cubic-bezier(0.34, 1.56, 0.64, 1)' });
        });
      });

      window.addEventListener('mousedown', () => {
        gsap.to(ring, { scale: 0.75, duration: 0.15, ease: 'power2.out' });
      });
      window.addEventListener('mouseup', () => {
        gsap.to(ring, { scale: 1, duration: 0.4, ease: 'cubic-bezier(0.34, 1.56, 0.64, 1)' });
      });

      return () => {
        window.removeEventListener('mousemove', onMouseMove);
        gsap.set([dot, ring], { autoAlpha: 0 });
        document.documentElement.style.cursor = '';
      };
    }
  );
})();
