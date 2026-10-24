#!/usr/bin/env python3
"""Optional asset-authoring step (Pillow required); normal builds use saved variants.

Original PNGs are kept unchanged for full-size viewing and format fallback.
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = {}
    for project in json.loads((ROOT / 'content/projects.json').read_text()):
        slug = project['slug']
        assets = ROOT / 'projects' / slug / 'assets'
        output = assets / 'responsive'
        output.mkdir(exist_ok=True)
        for source in sorted(assets.glob('*.png')):
            with Image.open(source) as original:
                if source.stem in ('app-icon', 'logo-512'):
                    widths = [56, 112, 224]
                else:
                    widths = [320, 480, 800, 1200, 1800, 2400, original.width]
                widths = sorted({min(w, original.width, 2400) for w in widths})
                variants = []
                for width in widths:
                    height = round(original.height * width / original.width)
                    resized = original.convert('RGBA').resize((width, height), Image.Resampling.LANCZOS)
                    target = output / f'{source.stem}-{width}.webp'
                    pet_illustration = slug == 'beewbe' and source.stem.startswith('pet-')
                    resized.save(target, 'WEBP', lossless=not pet_illustration, quality=90, method=6)
                    variants.append({'src': '/' + target.relative_to(ROOT).as_posix(), 'width': width})
                manifest['/' + source.relative_to(ROOT).as_posix()] = variants
    (ROOT / 'content/image-variants.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared responsive WebP variants for {len(manifest)} original images.')


if __name__ == '__main__':
    main()
