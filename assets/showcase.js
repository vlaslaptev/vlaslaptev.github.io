// Extend the native card link to its selectable copy without taking over dragging.
(() => {
  document.querySelectorAll('.project-card').forEach(card => {
    const link = card.querySelector('.project-card-link');
    const copy = card.querySelector('.card-copy');
    if (!link || !copy) return;

    let pointerStart = null;
    let dragged = false;
    let selectionBefore = '';
    copy.addEventListener('pointerdown', event => {
      pointerStart = { x: event.clientX, y: event.clientY, id: event.pointerId };
      dragged = false;
      selectionBefore = window.getSelection()?.toString() || '';
    });
    copy.addEventListener('pointermove', event => {
      if (!pointerStart || event.pointerId !== pointerStart.id || !event.buttons) return;
      if (Math.hypot(event.clientX - pointerStart.x, event.clientY - pointerStart.y) > 6) {
        dragged = true;
      }
    });
    copy.addEventListener('pointercancel', () => {
      pointerStart = null;
      dragged = true;
    });

    function activateLink(event) {
      if (event.defaultPrevented || (event.type === 'click' ? event.button !== 0 : event.button !== 1)) return;
      if (event.target.closest('a, button, input, select, textarea, [contenteditable]')) return;
      const selection = window.getSelection();
      const selectedText = selection?.toString() || '';
      // A previous selection must not disable the next ordinary click.
      if (dragged || (selectedText && selectedText !== selectionBefore && selection.containsNode(copy, true))) return;

      // Activate the real anchor. A middle click maps to the platform's new-tab modifier.
      const middleClick = event.button === 1;
      event.preventDefault();
      link.dispatchEvent(new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window,
        button: 0,
        detail: event.detail,
        ctrlKey: event.ctrlKey || middleClick,
        metaKey: event.metaKey || middleClick,
        shiftKey: event.shiftKey,
        altKey: event.altKey,
      }));
    }
    copy.addEventListener('click', activateLink);
    copy.addEventListener('auxclick', activateLink);
    card.classList.add('has-copy-link');
  });
})();

// Decorative motion. Native links and selectable content also work without JavaScript.
(() => {
  if (typeof window.matchMedia !== 'function') return;
  const motion = window.matchMedia('(prefers-reduced-motion: no-preference)');
  const cards = [...document.querySelectorAll('.project-card.variant-concept')];
  const timers = new Map();
  const seen = new WeakSet();

  function stop(card) {
    window.clearTimeout(timers.get(card));
    timers.delete(card);
    card.classList.remove('is-animating');
  }

  function animate(card) {
    if (!motion.matches || document.hidden || timers.has(card)) return;
    card.classList.add('is-animating');
    // Allow the longer sequences and their staggered starts to finish.
    const duration = card.classList.contains('tabs') ? 1600 : 2400;
    timers.set(card, window.setTimeout(() => stop(card), duration));
  }

  const observer = 'IntersectionObserver' in window
    ? new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {
          stop(entry.target);
          return;
        }
        if (!seen.has(entry.target) && motion.matches && !document.hidden) {
          animate(entry.target);
          seen.add(entry.target);
        }
      });
    }, { threshold: 0.35 })
    : null;

  cards.forEach(card => {
    if (observer) observer.observe(card);
    else animate(card);
    card.addEventListener('pointerenter', () => animate(card));
    card.addEventListener('focusin', event => {
      if (!card.contains(event.relatedTarget)) animate(card);
    });
  });

  function stopAll() { cards.forEach(stop); }
  function preferenceChanged() {
    if (!motion.matches) stopAll();
  }
  if (typeof motion.addEventListener === 'function') {
    motion.addEventListener('change', preferenceChanged);
  } else if (typeof motion.addListener === 'function') {
    motion.addListener(preferenceChanged);
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopAll();
  });
})();
