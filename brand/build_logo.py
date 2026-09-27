"""Build the "North Star" logo set for dkeikichi.com.

Wordmark: Archivo Expanded Black Italic (SIL Open Font License), converted to
outlines so the SVGs render the same everywhere. Star: original eight-point
needle star, tilted in perspective with the north-east heading ray extended.

    pip install fonttools uharfbuzz
    python3 brand/build_logo.py

Fonts are downloaded from Google Fonts into brand/.fonts/ on first run.
PNG/ICO files (favicon.ico, favicon-192, apple-touch-icon, og-image) are rendered from these
SVGs in a browser and are not produced by this script.
"""
import math
import os
import re
import urllib.request

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, '.fonts')
FONT_CSS = 'https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@1,125,900&display=swap'
FONT_FILE = os.path.join(FONT_DIR, 'ArchivoExpanded-BlackItalic.ttf')

NAVY, BLUE, SKY, SKY_LIGHT = '#062a56', '#0b4d94', '#2f7fe0', '#7db9f0'
PALETTES = {
    # navy wordmark with a bright-blue star, so the star still reads on dark backgrounds
    'color': dict(word=NAVY, lit=SKY_LIGHT, shade=SKY, lit2='#b9dafa', shade2='#5a9ff0'),
    'white': dict(word='#ffffff', lit='#ffffff', shade='#9cc8f4', lit2='#cfe3fa', shade2=SKY_LIGHT),
}
LIGHT_DIR = (-0.6, -0.8)   # rays are lit from the upper left


def fmt(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


def ensure_font():
    if os.path.exists(FONT_FILE):
        return
    os.makedirs(FONT_DIR, exist_ok=True)
    req = urllib.request.Request(FONT_CSS, headers={'User-Agent': 'Mozilla/5.0'})
    css = urllib.request.urlopen(req).read().decode()
    url = re.search(r'url\((https://[^)]+\.ttf)\)', css).group(1)
    urllib.request.urlretrieve(url, FONT_FILE)


def text_path(text, size, tracking):
    """Outline `text` with kerning; baseline at y=0. Returns (d, ink_bounds, cap_height)."""
    tt = TTFont(FONT_FILE)
    gs, order = tt.getGlyphSet(), tt.getGlyphOrder()
    font = hb.Font(hb.Face(hb.Blob.from_file_path(FONT_FILE)))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True})
    s = size / tt['head'].unitsPerEm
    x, parts, box = 0.0, [], None
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyph = gs[order[info.codepoint]]
        m = (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s)
        pen = SVGPathPen(gs, ntos=fmt)
        glyph.draw(TransformPen(pen, m))
        parts.append(pen.getCommands())
        bp = BoundsPen(gs)
        glyph.draw(TransformPen(bp, m))
        if bp.bounds:
            b = bp.bounds
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        x += pos.x_advance * s + tracking * size
    return ' '.join(parts), box, tt['OS/2'].sCapHeight * s


def ray(pts, cx, cy, ang, length, w, light, dark):
    """A needle ray: thin wedge from the centre, split along its axis into lit and shaded halves."""
    a = math.radians(ang)
    tx, ty = cx + length * math.cos(a), cy + length * math.sin(a)
    px, py = -math.sin(a) * w, math.cos(a) * w
    pts += [(tx, ty), (cx + px, cy + py), (cx - px, cy - py)]
    c1, c2 = (light, dark) if px * LIGHT_DIR[0] + py * LIGHT_DIR[1] > 0 else (dark, light)
    return (f'<path d="M{fmt(cx)} {fmt(cy)} L{fmt(tx)} {fmt(ty)} L{fmt(cx + px)} {fmt(cy + py)} Z" fill="{c1}"/>'
            f'<path d="M{fmt(cx)} {fmt(cy)} L{fmt(tx)} {fmt(ty)} L{fmt(cx - px)} {fmt(cy - py)} Z" fill="{c2}"/>')


def north_star(p, weight=1.0):
    """Eight-point star in perspective. Returns (svg, ink_bounds) in a 100x100 box."""
    pts = []
    minor = [(-135, 22, 2.6), (135, 22, 2.6), (45, 24, 2.6)]
    major = [(-90, 48, 5.0), (0, 44, 5.0), (90, 42, 5.0), (180, 34, 5.0)]
    heading = [(-45, 66, 3.6)]
    body = ''.join(ray(pts, 50, 50, a, l, w * weight, p['lit2'], p['shade2']) for a, l, w in minor)
    body += ''.join(ray(pts, 50, 50, a, l, w * weight, p['lit'], p['shade']) for a, l, w in major + heading)
    # tilt: x' = x - 0.16 y, y' = 0.92 y (about the centre), shifted down by 1
    body = f'<g transform="translate(50 51) matrix(1 0 -0.16 0.92 0 0) translate(-50 -50)">{body}</g>'
    tp = [((x - 50) - 0.16 * (y - 50) + 50, 0.92 * (y - 50) + 51) for x, y in pts]
    xs, ys = [x for x, _ in tp], [y for _, y in tp]
    return body, (min(xs), min(ys), max(xs), max(ys))


def svg(viewbox, body, title='Keikichi Den'):
    vb = ' '.join(fmt(v) for v in viewbox)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def lockup(p, size):
    """Wordmark + star. `size` is the star's ink height in cap heights (5 = full logo, 2.4 = header)."""
    name_d, nb, cap = text_path('KEIKICHI DEN', 100, tracking=0.12)
    name_w = nb[2] - nb[0]
    star, (bx0, by0, bx1, by1) = north_star(p)
    sc = size * cap / (by1 - by0)
    sx = name_w + cap * (0.35 + 0.05 * size) - bx0 * sc
    sy = -cap * 0.5 - (size - 1) * cap * 0.14 - (by0 + by1) / 2 * sc
    body = (f'<path d="{name_d}" transform="translate({fmt(-nb[0])} 0)" fill="{p["word"]}"/>'
            f'<g transform="translate({fmt(sx)} {fmt(sy)}) scale({sc:.4f})">{star}</g>')
    top, bottom, right = min(sy + by0 * sc, -cap), max(sy + by1 * sc, 0), sx + bx1 * sc
    pad = 4
    return svg((-pad, top - pad, right + 2 * pad, bottom - top + 2 * pad), body)


def app_mark():
    """Star on a rounded navy tile, for favicons and home-screen icons."""
    star, (x0, y0, x1, y1) = north_star(PALETTES['white'], weight=1.9)
    side = max(x1 - x0, y1 - y0)
    sc = 76 / side
    tx, ty = 50 - (x0 + x1) / 2 * sc, 50 - (y0 + y1) / 2 * sc
    body = (f'<rect width="100" height="100" rx="22" fill="{BLUE}"/>'
            f'<g transform="translate({fmt(tx)} {fmt(ty)}) scale({sc:.4f})">{star}</g>')
    return svg((0, 0, 100, 100), body)


if __name__ == '__main__':
    ensure_font()
    outputs = {
        'logo.svg': lockup(PALETTES['color'], 5.0),
        'logo-white.svg': lockup(PALETTES['white'], 5.0),
        'logo-compact.svg': lockup(PALETTES['color'], 2.4),
        'logo-compact-white.svg': lockup(PALETTES['white'], 2.4),
        'mark.svg': app_mark(),
    }
    for name, data in outputs.items():
        with open(os.path.join(HERE, name), 'w') as f:
            f.write(data)
        print('wrote', name)
