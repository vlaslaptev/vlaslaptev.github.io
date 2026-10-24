#!/usr/bin/env python3
"""Check the site's local links, fragments, images, metadata and file boundary."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.preview', '__pycache__'}
FORBIDDEN = {'.swift', '.kt', '.java', '.class', '.jar', '.dmg', '.ipa', '.zip', '.p12', '.mobileprovision', '.key', '.log'}


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.errors = []
        self.headings = 0
        self.title = False
        self.description = False
        self.lang = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append(f'duplicate id: {a["id"]}')
            self.ids.add(a['id'])
        if tag == 'h1': self.headings += 1
        if tag == 'html': self.lang = bool(a.get('lang'))
        if tag == 'title': self.title = True
        if tag == 'meta' and a.get('name') == 'description': self.description = bool(a.get('content'))
        if tag == 'meta' and a.get('property') == 'og:image': self.links.append(a.get('content', ''))
        if tag == 'img' and 'alt' not in a: self.errors.append('image without alt')
        for key in ('href', 'src'):
            if a.get(key): self.links.append(a[key])
        if a.get('srcset'):
            self.links.extend(item.strip().split()[0] for item in a['srcset'].split(','))


def local_path(source, href):
    url = urlsplit(href)
    if (url.scheme or url.netloc) and url.netloc != 'vlaslaptev.github.io':
        return None, None
    path = unquote(url.path)
    target = (ROOT / path.lstrip('/')) if path.startswith('/') else source.parent / path if path else source
    target = target.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError(f'link escapes site: {href}')
    if target.is_dir(): target /= 'index.html'
    return target, unquote(url.fragment)


def main():
    documents = {}
    errors = []
    files = [p for p in ROOT.rglob('*') if p.is_file() and not any(part in EXCLUDED for part in p.relative_to(ROOT).parts)]
    for p in files:
        if p.suffix.lower() in FORBIDDEN or '.xcodeproj' in p.parts:
            errors.append(f'Non-website file: {p.relative_to(ROOT)}')
        if p.suffix == '.html' and 'templates' not in p.relative_to(ROOT).parts:
            d = Document(p)
            d.feed(p.read_text())
            if d.headings != 1: d.errors.append(f'{d.headings} H1 headings')
            if not d.title or not d.description or not d.lang: d.errors.append('missing title, description or language')
            documents[p] = d
    count = 0
    for p, d in documents.items():
        errors.extend(f'{p.relative_to(ROOT)}: {error}' for error in d.errors)
        for link in d.links:
            count += 1
            try:
                target, fragment = local_path(p, link)
            except ValueError as error:
                errors.append(f'{p.relative_to(ROOT)}: {error}')
                continue
            if target is None: continue
            if not target.is_file(): errors.append(f'{p.relative_to(ROOT)}: missing {link}')
            elif fragment and target in documents and fragment not in documents[target].ids:
                errors.append(f'{p.relative_to(ROOT)}: missing fragment {link}')
    for p in files:
        if p.suffix == '.css':
            for value in re.findall(r'url\(\s*[\'"]?([^\)\'\"]+)',p.read_text()):
                target,_ = local_path(p, value.strip())
                if target is not None and not target.is_file(): errors.append(f'{p.relative_to(ROOT)}: missing CSS resource {value}')
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print(f'OK: {len(documents)} pages, {count} links/resources, one H1 per page, metadata, image alt text, local fragments, no application source or binaries.')


if __name__ == '__main__':
    main()
