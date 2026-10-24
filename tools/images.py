"""Render pre-generated responsive assets. No image library needed for site builds."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def responsive_images(markup, page_path='index.html', lang='en'):
    manifest = json.loads((ROOT / 'content/image-variants.json').read_text())

    def replace(match):
        tag = match.group(0)
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
        source = urlsplit(html.unescape(attrs.get('src', ''))).path
        if not source:
            return tag
        path = ROOT / source.lstrip('/') if source.startswith('/') else ROOT / Path(page_path).parent / source
        key = '/' + path.resolve().relative_to(ROOT).as_posix()
        variants = manifest.get(key)
        if not variants:
            return tag
        sizes = attrs.get('data-sizes', '(max-width: 700px) calc(100vw - 40px), (min-width: 1800px) 1320px, (min-width: 1280px) 1200px, calc(100vw - 80px)')
        tag = re.sub(r' data-(?:sizes|fullsize)="[^"]*"', '', tag)
        sources = ', '.join(f'{v["src"]} {v["width"]}w' for v in variants)
        result = f'<picture class="responsive-image"><source type="image/webp" srcset="{sources}" sizes="{html.escape(sizes, quote=True)}">{tag}</picture>'
        if 'data-fullsize' in attrs:
            label = 'Открыть в полном размере' if lang == 'ru' else 'View full size'
            name = html.escape(label + ': ' + html.unescape(attrs.get('alt', '')), quote=True)
            result = f'<a class="image-link" href="{key}" target="_blank" rel="noopener" aria-label="{name}">{result}<span class="image-hint">{label} <span aria-hidden="true">↗</span></span></a>'
        return result

    return re.sub(r'<img\b[^>]*>', replace, markup)
