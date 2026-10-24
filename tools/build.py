#!/usr/bin/env python3
"""Generate the portfolio and new landing pages. Standard library only.

Imported product pages are intentionally not regenerated or reformatted.
"""
import html
import hashlib
import json
import re
import struct
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from urllib.parse import urlsplit
from images import responsive_images

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://vlaslaptev.github.io'
EMAIL = 'vlas.developer@icloud.com'
TEXT = {
    'en': {
        'name': 'Vlas Laptev', 'title': 'Vlas Laptev — Independent developer',
        'description': 'Useful tools and little worlds. Discover Project Tab Icons, beewbe, BatteryGrid for Mac and Pet Project by independent developer Vlas Laptev.',
        'projects': 'Projects', 'contact': 'Contact', 'skip': 'Skip to content',
        'headline': 'Useful tools. <span>Little worlds.</span>',
        'intro': 'Apps, widgets and IDE tools. Made with care.',
        'selected': 'Selected projects', 'learn': 'Explore project',
        'write': 'Email me', 'back': 'All projects', 'top': 'Back to top ↑', 'footer': 'Independent software, made with care.',
        'missing': 'This page has moved on.', 'missing_copy': 'The old site has a new home for apps, widgets and developer tools. Find your next stop in the project collection.',
    },
    'ru': {
        'name': 'Влас Лаптев', 'title': 'Влас Лаптев — разработчик приложений и виджетов',
        'description': 'Полезные инструменты и маленькие миры. Project Tab Icons, beewbe, BatteryGrid для Mac и Pet Project — проекты разработчика Власа Лаптева.',
        'projects': 'Проекты', 'contact': 'Контакты', 'skip': 'Перейти к содержимому',
        'headline': 'Полезные инструменты. <span>Маленькие миры.</span>',
        'intro': 'Приложения, виджеты и инструменты для IDE.',
        'selected': 'Мои проекты', 'learn': 'О проекте',
        'write': 'Написать', 'back': 'Все проекты', 'top': 'Наверх ↑', 'footer': 'Независимые проекты. С вниманием к деталям.',
        'missing': 'У этой страницы новая история.', 'missing_copy': 'На смену старому сайту пришла витрина приложений, виджетов и инструментов. Выберите проект на главной странице.',
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def write(path, content):
    target = ROOT / path.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')


def fingerprint_assets():
    """Refresh local CSS/JS URLs, including references in imported static pages."""
    for page_path in ROOT.rglob('*.html'):
        if any(part in {'templates', '.preview', '.git'} for part in page_path.relative_to(ROOT).parts):
            continue
        original = page_path.read_text()
        def replace(match):
            url = urlsplit(match[2])
            if url.scheme or url.netloc or not url.path.endswith(('.css', '.js')):
                return match[0]
            asset = ROOT / url.path.lstrip('/') if url.path.startswith('/') else page_path.parent / url.path
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
            return f'{match[1]}="{url.path}?v={digest}"'
        updated = re.sub(r'(href|src)="([^"]+)"', replace, original)
        if updated != original:
            page_path.write_text(updated)


def image_dimensions(markup):
    """Reserve intrinsic PNG dimensions without a third-party image dependency."""
    def replace(match):
        tag = match.group(0)
        source = re.search(r'src="([^"]+)"', tag)
        if not source:
            return tag
        path = ROOT / source.group(1).lstrip('/')
        if path.suffix != '.png' or not path.is_file():
            return tag
        with path.open('rb') as image:
            header = image.read(24)
        if header[:8] != b'\x89PNG\r\n\x1a\n':
            return tag
        width, height = struct.unpack('>II', header[16:24])
        if 'width=' not in tag:
            tag = tag[:-1] + f' width="{width}" height="{height}">'
        return tag
    return re.sub(r'<img\b[^>]*>', replace, markup)


def language_nav(lang, urls):
    links = []
    for code in ('en', 'ru'):
        current = ' aria-current="page"' if code == lang else ''
        links.append(f'<a href="{esc(urls[code])}" lang="{code}" hreflang="{code}"{current}>{code.upper()}</a>')
    return '<nav class="language" aria-label="Language / Язык">' + ''.join(links) + '</nav>'


def page(lang, title, description, url, body, css_class='', alternate=None, image='/assets/social-preview.png'):
    canonical = DOMAIN + url
    showcase_styles = '  <link rel="stylesheet" href="/assets/showcase.css">\n' if css_class == 'home-page' else ''
    showcase_script = '  <script src="/assets/showcase.js" defer></script>\n' if css_class == 'home-page' else ''
    theme_meta = ('  <meta name="color-scheme" content="dark light">\n'
                  '  <meta name="theme-color" content="#f5f5f7" media="(prefers-color-scheme: light)">\n'
                  '  <meta name="theme-color" content="#111216">\n') if css_class == 'home-page' else (
                  '  <meta name="color-scheme" content="light">\n'
                  '  <meta name="theme-color" content="#f5f5f7">\n')
    alternate_links = ''.join(f'<link rel="alternate" hreflang="{code}" href="{DOMAIN}{esc(path)}">' for code, path in (alternate or {}).items())
    if alternate:
        alternate_links += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{esc(alternate["en"])}">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{theme_meta}  <meta name="description" content="{esc(description)}">
  <meta name="author" content="Vlas Laptev">
  <title>{esc(title)}</title>
  <link rel="canonical" href="{canonical}">
  {alternate_links}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}{image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css">
{showcase_styles}  <script src="/assets/site.js" defer></script>
{showcase_script}{'  <script src="/assets/portfolio-link.js" defer></script>' if css_class == 'product-page' else ''}</head>
<body class="{css_class}" id="top">
<a class="skip-link" href="#main">{TEXT[lang]['skip']}</a>
{responsive_images(image_dimensions(body), lang=lang) if css_class == 'product-page' else image_dimensions(body)}
</body>
</html>
'''


def card_visual(item, lang, variant):
    card = item['card']
    if variant == 'icon':
        return f'<img class="card-icon" src="{esc(card["icon"])}" alt="" decoding="async">'
    if variant == 'interface':
        return f'<img class="interface-image" src="{esc(card["interface"].replace("{lang}", lang))}" alt="" decoding="async">'
    if item['theme'] == 'tabs':
        return '<div class="tab-scene"><span class="tab-tile">{ }</span><span class="tab-tile">&lt;/&gt;</span><span class="tab-tile">⌘</span></div>'
    if item['theme'] == 'beewbe':
        eyelids = '''<svg class="pet-eyelids" viewBox="0 0 640 640">
          <ellipse cx="246" cy="244" rx="25" ry="28"/><ellipse cx="394" cy="244" rx="25" ry="28"/>
          <path d="M231 241q15 13 30 0M379 241q15 13 30 0"/>
        </svg>'''
        return '<div class="pet-friends">' + ''.join(f'<span class="pet-friend {color}">{card_thumbnail("beewbe-" + color, 72 if color == "mint" else 54)}{eyelids}</span>' for color in ('lavender', 'mint', 'sky')) + '</div>'
    if item['theme'] == 'battery':
        return '''<div class="charge-scene">
          <span class="charge-orbit"><svg viewBox="0 0 24 24"><path d="M5 5h14v11H5zM2 19h20"/></svg></span>
          <span class="charge-orbit"><svg viewBox="0 0 24 24"><rect x="7" y="3" width="10" height="18" rx="5"/><path d="M12 3v6"/></svg></span>
          <span class="charge-orbit"><svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="11" rx="2"/><path d="M6 10h12M6 13h12M8 16h8"/></svg></span>
        </div>'''
    if item['theme'] == 'pet':
        return f'<div class="pixel-scene"><span class="pixel-star"></span><span class="pixel-building"></span><span class="pixel-building"></span>{card_thumbnail("pet-project", 44)}<span class="pixel-building"></span></div>'
    if item['theme'] == 'garnet':
        return '''<svg class="garnet-cycle" viewBox="0 0 80 80" focusable="false">
          <path d="M47 13a28 28 0 0 1 20 20"/>
          <path d="M47 13a28 28 0 0 1 20 20" transform="rotate(90 40 40)"/>
          <path d="M47 13a28 28 0 0 1 20 20" transform="rotate(180 40 40)"/>
          <path d="M47 13a28 28 0 0 1 20 20" transform="rotate(270 40 40)"/>
        </svg>'''
    return f'<div class="icon-orbit"><img class="card-icon" src="{esc(card["icon"])}" alt="" decoding="async"></div>'


def card_thumbnail(name, size):
    """Small decorative assets with density variants; originals stay on product pages."""
    base = '/assets/card-thumbnails/' + name
    def sources(extension):
        return ', '.join(f'{base}{suffix}.{extension} {density}x'
                         for density, suffix in ((1, ''), (2, '@2x'), (3, '@3x')))
    return (f'<picture><source type="image/webp" srcset="{sources("webp")}">'
            f'<img src="{base}.png" srcset="{sources("png")}" alt="" '
            f'width="{size}" height="{size}" decoding="async"></picture>')


def home(lang, projects, variants):
    t = TEXT[lang]
    home_url = '/' if lang == 'en' else '/ru/'
    cards = []
    variant_names = {'en': {'icon': 'Icon', 'interface': 'Interface', 'concept': 'Character'},
                     'ru': {'icon': 'Иконка', 'interface': 'Интерфейс', 'concept': 'Характер'}}
    availability_names = {'en': {'available': 'Available', 'beta': 'TestFlight beta', 'development': 'In development'},
                          'ru': {'available': 'Доступно', 'beta': 'Бета в TestFlight', 'development': 'В разработке'}}
    for number, variant in enumerate(variants, 1):
        for item in projects:
            note = item.get('link_note', {}).get(lang, '')
            label = t['learn'] + ': ' + item['name']
            card_id = item['slug'] if variant == variants[0] else item['slug'] + '-' + variant
            note_markup = f'<small class="card-link-note" id="{esc(card_id)}-note">{esc(note)}</small>' if note else ''
            describedby = f'{card_id}-status {card_id}-description' + (f' {card_id}-note' if note else '')
            # Enter every product in English; translations remain explicit choices.
            url = item['url']['en'] + f'?from={lang}'
            variant_name = f'{number:02d} · {variant_names[lang][variant]}'
            badge = f'<span class="card-variant" title="{variant_name}" aria-hidden="true">{number:02d}</span>' if len(variants) > 1 else ''
            label += ' · ' + variant_name if len(variants) > 1 else ''
            cards.append(f'''<article class="project-card {esc(item['theme'])} variant-{variant}" id="{esc(card_id)}" data-variant="{variant}">
  <a class="project-card-link" href="{esc(url)}" draggable="false" aria-label="{esc(label)}" aria-describedby="{esc(describedby)}">
    <div class="card-visual" aria-hidden="true">{card_visual(item, lang, variant)}</div>{badge}
    <span class="card-arrow" aria-hidden="true">↗</span>
  </a>
  <div class="card-copy"><span class="card-status availability-{item['availability']}" id="{esc(card_id)}-status"><span class="status-dot" aria-hidden="true"></span>{availability_names[lang][item['availability']]}</span><h3>{esc(item['name'])}</h3><p id="{esc(card_id)}-description">{esc(item['card']['description'][lang])}</p>{note_markup}</div>
</article>''')
    body = f'''<header class="site-header home-header"><div class="navigation wrap">
  <a class="wordmark" href="{home_url}">{t['name']}</a>
  <nav class="nav-links" aria-label="{'Main navigation' if lang == 'en' else 'Основная навигация'}"><a href="#projects">{t['projects']}</a><a href="#contact">{t['contact']}</a></nav>
  {language_nav(lang, {'en':'/', 'ru':'/ru/'})}
</div></header>
<main id="main" tabindex="-1">
  <section class="home-hero" aria-labelledby="hero-title">
    <h1 id="hero-title">{t['headline']}</h1><p class="intro">{t['intro']}</p>
  </section>
  <section class="work" id="projects" aria-labelledby="projects-title"><div class="wrap">
    <div class="section-top"><h2 id="projects-title">{t['selected']}</h2></div>
    <div class="project-grid">{''.join(cards)}</div>
  </div></section>
  <section class="contact" id="contact" aria-labelledby="contact-title"><div class="wrap"><h2 id="contact-title">{t['contact']}</h2>
    <div class="contact-links"><a class="text-link" href="mailto:{EMAIL}">{EMAIL} <span aria-hidden="true">↗</span></a><a class="text-link" href="https://github.com/vlaslaptev">GitHub <span aria-hidden="true">↗</span></a></div>
  </div></section>
</main>
<footer class="footer"><div class="wrap"><p>© 2026 {t['name']}. {t['footer']}</p><div class="footer-links"><a href="#top">{t['top']}</a></div></div></footer>'''
    write('index.html' if lang == 'en' else 'ru/index.html', page(lang, t['title'], t['description'], home_url, body, 'home-page', alternate={'en':'/', 'ru':'/ru/'}))


def landing(item, lang):
    t = TEXT[lang]
    template = ROOT / 'templates' / f'{item["slug"]}.{lang}.html'
    if not template.exists():
        return
    home_url = '/' if lang == 'en' else '/ru/'
    body = f'''<header class="site-header product-header"><div class="navigation wrap"><a class="back-link" href="{home_url}#projects" data-portfolio-return><span aria-hidden="true">‹</span> <span data-portfolio-return-label>{t['back']}</span></a><a class="wordmark" href="{item['url'][lang]}">{esc(item['name'])}</a>{language_nav(lang,item['url'])}</div></header>
{template.read_text()}
<footer class="product-footer"><p>© 2026 {t['name']} · {esc(item['name'])}</p><a href="{home_url}#projects" data-portfolio-return><span data-portfolio-return-label>{t['back']}</span></a><a href="mailto:{EMAIL}">{t['write']}</a></footer>'''
    write(item['url'][lang] + 'index.html', page(lang, item['name'] + ' — ' + item['description'][lang], item['detail'][lang], item['url'][lang], body, 'product-page', item['url'], item['images'][0]['src'].replace('{lang}',lang)))


def main():
    projects = json.loads((ROOT / 'content/projects.json').read_text())
    if any(item.get('availability') not in {'available', 'beta', 'development'} for item in projects):
        raise ValueError('Every project needs an availability: available, beta or development')
    variants = json.loads((ROOT / 'content/showcase.json').read_text())['card_variants']
    if not variants or len(variants) != len(set(variants)) or any(v not in {'icon', 'interface', 'concept'} for v in variants):
        raise ValueError('Choose unique card variants: icon, interface, concept')
    slugs = [item['slug'] for item in projects]
    if len(slugs) != len(set(slugs)) or any(not re.fullmatch(r'[a-z0-9-]+', slug) for slug in slugs):
        raise ValueError('Project slugs must be unique, lowercase and URL-safe')
    projects.sort(key=lambda item: item['order'])
    for lang in ('en', 'ru'):
        home(lang, projects, variants)
        for item in projects:
            landing(item, lang)
    t = TEXT['en']
    body = f'<main id="main" tabindex="-1" class="not-found"><p class="eyebrow">404</p><h1>{t["missing"]}</h1><p>{t["missing_copy"]}</p><div class="actions"><a class="pill" href="/#projects">All projects</a><a class="text-link" href="/ru/">Русский →</a></div></main>'
    write('404.html', page('en','Page not found — Vlas Laptev',t['missing_copy'],'/404.html',body))
    urls = []
    for p in sorted(ROOT.rglob('*.html')):
        if any(part in {'templates','.git','.preview'} for part in p.relative_to(ROOT).parts) or p.name == '404.html':
            continue
        url = '/' + p.relative_to(ROOT).as_posix()
        if url.endswith('index.html'):
            url = url[:-10]
        urls.append(DOMAIN + url)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{xml_escape(url)}</loc></url>\n' for url in urls) + '</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    fingerprint_assets()
    print(f'Generated EN/RU portfolio and product pages; sitemap contains {len(urls)} pages.')


if __name__ == '__main__':
    main()
