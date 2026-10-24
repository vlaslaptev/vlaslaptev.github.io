// Explicit entry language also works after reloads and opening a card in a new tab.
// Page language is an explicit choice; this only remembers the portfolio entry.
(() => {
  const header = document.querySelector('.site-header, .header');
  if (header) {
    const measure = () => document.documentElement.style.setProperty('--product-nav-height', `${header.getBoundingClientRect().height}px`);
    measure();
    if ('ResizeObserver' in window) new ResizeObserver(measure).observe(header);
  }
  const from = new URLSearchParams(window.location.search).get('from');
  if (from === 'ru' || from === 'en') {
    document.querySelectorAll('[data-portfolio-return], a[href="/#projects"], a[href="/ru/#projects"]').forEach(link => {
      if (link.closest('[data-portfolio-return-fallback]')) return;
      link.href = from === 'ru' ? '/ru/#projects' : '/#projects';
      const label = link.querySelector('[data-portfolio-return-label]');
      if (label) {
        label.textContent = from === 'ru' ? 'Все проекты' : 'All projects';
        link.lang = from;
      }
    });
    const productRoot = window.location.pathname.match(/^\/projects\/[^/]+\//)?.[0];
    document.querySelectorAll('a[href]').forEach(link => {
      if (link.getAttribute('href').startsWith('#')) return;
      const url = new URL(link.href);
      if (url.origin === window.location.origin && productRoot && url.pathname.startsWith(productRoot) && /(?:\/|\.html)$/.test(url.pathname)) {
        url.searchParams.set('from', from);
        link.href = url.pathname + url.search + url.hash;
      }
    });
  }
  document.querySelectorAll('[data-portfolio-return-fallback]').forEach(link => { link.hidden = true; });
})();
