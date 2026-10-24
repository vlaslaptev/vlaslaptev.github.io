/* Local presentation only. No requests, storage, cookies or language detection. */
(() => {
  'use strict';
  const root = document.documentElement;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const hero = document.querySelector('.hero');
  const story = document.querySelector('.product-story');
  const header = document.querySelector('.header');
  const language = document.querySelector('.language');
  const motionToggle = document.querySelector('[data-motion-toggle]');
  const motionDisabled = () => reducedMotion.matches || root.classList.contains('motion-off');
  let frame = 0;
  let observer;
  const clamp = value => Math.min(1, Math.max(0, value));

  function paintScroll() {
    frame = 0;
    if (motionDisabled()) return;
    const height = window.innerHeight;
    if (hero) {
      const rect = hero.getBoundingClientRect();
      if (rect.bottom >= 0 && rect.top <= height) {
        hero.style.setProperty('--hero-progress', clamp(-rect.top / rect.height).toFixed(4));
      }
    }
    if (story) {
      const rect = story.getBoundingClientRect();
      if (rect.bottom >= 0 && rect.top <= height) {
        const range = Math.max(1, rect.height - height * .4);
        story.style.setProperty('--story-progress', clamp((height * .65 - rect.top) / range).toFixed(4));
      }
    }
  }
  function requestPaint() {
    if (!frame && !motionDisabled()) frame = requestAnimationFrame(paintScroll);
  }
  function syncHeader() {
    if (header) root.style.setProperty('--nav-height', `${header.getBoundingClientRect().height}px`);
    requestPaint();
  }
  function setupMotion() {
    root.classList.toggle('motion', !motionDisabled());
    if (motionToggle) {
      motionToggle.setAttribute('aria-pressed', String(motionDisabled()));
      motionToggle.disabled = reducedMotion.matches;
    }
    if (observer) observer.disconnect();
    document.querySelectorAll('.reveal').forEach(element => {
      element.getAnimations?.().forEach(animation => animation.cancel());
    });
    if (motionDisabled()) {
      cancelAnimationFrame(frame);
      frame = 0;
      hero?.style.removeProperty('--hero-progress');
      story?.style.removeProperty('--story-progress');
      return;
    }
    if ('IntersectionObserver' in window) {
      observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          observer.unobserve(entry.target);
          if (!entry.target.animate) return;
          entry.target.animate([
            { opacity: 0, transform: 'translateY(32px)' },
            { opacity: 1, transform: 'translateY(0)' }
          ], { duration: 850, easing: 'cubic-bezier(.22,1,.36,1)' });
        });
      }, { threshold: .12 });
      document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
    }
    requestPaint();
  }
  document.querySelectorAll('.swatch').forEach(button => {
    button.addEventListener('click', () => {
      const color = button.dataset.color;
      document.querySelectorAll('.swatch').forEach(swatch => {
        swatch.setAttribute('aria-pressed', String(swatch === button));
      });
      document.querySelectorAll('.look-image').forEach(image => {
        image.classList.toggle('selected', image.dataset.look === color);
      });
      document.querySelector('.look-label').textContent = button.getAttribute('aria-label');
    });
  });
  document.querySelectorAll('.look-controls').forEach(element => { element.hidden = false; });
  if (motionToggle) {
    motionToggle.hidden = false;
    motionToggle.addEventListener('click', () => {
      root.classList.toggle('motion-off');
      setupMotion();
    });
  }
  if (language) {
    document.addEventListener('click', event => {
      if (!language.contains(event.target)) language.open = false;
    });
    language.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        language.open = false;
        language.querySelector('summary').focus();
      }
    });
  }
  window.addEventListener('scroll', requestPaint, { passive: true });
  window.addEventListener('resize', syncHeader, { passive: true });
  if ('ResizeObserver' in window && header) new ResizeObserver(syncHeader).observe(header);
  reducedMotion.addEventListener('change', setupMotion);
  setupMotion();
  syncHeader();
})();
