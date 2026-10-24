// The pages, links and gallery images remain usable without JavaScript.
document.querySelectorAll('[data-gallery]').forEach(gallery => {
  const controls = gallery.querySelector('[data-gallery-controls]');
  const panels = [...gallery.querySelectorAll('[data-panel]')];
  const buttons = [...gallery.querySelectorAll('[data-show]')];
  if (!controls || !panels.length || !buttons.length) return;
  function select(id) {
    panels.forEach(panel => { panel.hidden = panel.id !== id; });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.show === id)));
  }
  controls.hidden = false;
  gallery.dataset.galleryReady = '';
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.show)));
  select(buttons[0].dataset.show);
});
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const elements = [...document.querySelectorAll('.reveal')];
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.04 });
  document.documentElement.classList.add('motion-ready');
  elements.forEach(element => observer.observe(element));
  // Never leave content invisible if the observer cannot run in a background tab.
  window.setTimeout(() => elements.forEach(element => element.classList.add('visible')), 4000);
}
