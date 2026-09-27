"""Build the English (/) and Japanese (/ja/) pages from one bilingual template.

Edit _src/index.template.html, then run:

    python3 _src/build_pages.py

The template holds both languages side by side: elements with class
"lang-en" or "lang-ja", and attributes written as attr="English"
data-ja-attr="日本語". Each output keeps only its own language, gets its own
<head> (title, description, canonical, hreflang, structured data), and the
sitemap is regenerated. _src/ is not published (Jekyll skips "_" folders).
"""
import datetime
import json
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, '_src', 'index.template.html')
SITE = 'https://dkeikichi.com'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

PAGES = {
    'en': dict(
        out='index.html',
        url=f'{SITE}/',
        title='Keikichi Den (田 慶吉) — IT Engineer at ANA Systems',
        description=('Keikichi Den (田 慶吉), IT engineer at ANA Systems in Tokyo — network infrastructure, '
                     'cloud VDI and endpoint security. Formerly Lenovo Japan, Nippon Express and AGC.'),
        og_title='Keikichi Den (田 慶吉) — IT Engineer',
        og_description='IT engineer at ANA Systems in Tokyo — network infrastructure, cloud VDI and endpoint security.',
        og_locale='en_US', og_locale_alt='ja_JP',
        # A visitor whose saved language is Japanese goes to /ja/. Only a saved choice
        # triggers this, never the browser language, so crawlers always get this page.
        head_script='''        (function () {
            try {
                if (localStorage.getItem('lang') === 'ja') { location.replace('/ja/' + location.hash); return; }
            } catch (e) {}
            // Scroll-reveal hides cards until script.js shows them; only opt in when JS runs.
            document.documentElement.className += ' js';
        })();''',
    ),
    'ja': dict(
        out='ja/index.html',
        url=f'{SITE}/ja/',
        title='田 慶吉（デン ケイキチ）｜ANAシステムズ ITエンジニア',
        description=('ANAシステムズ所属のITエンジニア、田 慶吉（デン ケイキチ / Keikichi Den）のポートフォリオ。'
                     'ネットワークインフラの設計・保守、大規模VDIのクラウド移行、端末・セキュリティ管理を担当。'
                     'レノボ・ジャパン、日本通運、AGCでの経験。'),
        og_title='田 慶吉（デン ケイキチ）｜ITエンジニア',
        og_description='ANAシステムズのITエンジニア。ネットワークインフラ、大規模VDIのクラウド移行、端末・セキュリティ管理。',
        og_locale='ja_JP', og_locale_alt='en_US',
        head_script='''        // Scroll-reveal hides cards until script.js shows them; only opt in when JS runs.
        document.documentElement.className += ' js';''',
    ),
}

PERSON = {
    '@type': 'Person',
    '@id': f'{SITE}/#person',
    'name': 'Keikichi Den',
    'alternateName': ['田 慶吉', 'デン ケイキチ'],
    'url': f'{SITE}/',
    'image': f'{SITE}/IMG_1545.JPG',
    'jobTitle': 'IT Engineer',
    'worksFor': {'@type': 'Organization', 'name': 'ANA Systems Co., Ltd.', 'alternateName': 'ANAシステムズ株式会社'},
    'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Tokyo City University', 'alternateName': '東京都市大学',
                 'url': 'https://www.tcu.ac.jp/'},
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Tokyo', 'addressCountry': 'JP'},
    'knowsAbout': ['Network infrastructure', 'Virtual desktop infrastructure (VDI)', 'Endpoint security',
                   'Windows deployment', 'Microsoft Intune', 'Windows Autopilot', 'PowerShell', 'Python', 'RPA'],
    'sameAs': ['https://www.linkedin.com/in/keikichi-d-5282451a9'],
}


def jsonld(lang, page):
    graph = [
        {'@type': 'WebSite', '@id': f'{SITE}/#website', 'url': f'{SITE}/', 'name': 'Keikichi Den',
         'alternateName': ['田 慶吉', 'dkeikichi.com'], 'inLanguage': ['en', 'ja'],
         'publisher': {'@id': f'{SITE}/#person'}},
        {'@type': 'ProfilePage', '@id': f'{page["url"]}#profile', 'url': page['url'], 'name': page['title'],
         'inLanguage': lang, 'isPartOf': {'@id': f'{SITE}/#website'}, 'mainEntity': {'@id': f'{SITE}/#person'}},
        PERSON,
    ]
    text = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=4)
    return '\n'.join('    ' + line for line in text.splitlines())


class _Ranges(HTMLParser):
    """Collect [start, end) offsets of every element carrying `cls`, including its children."""

    def __init__(self, src, cls):
        super().__init__(convert_charrefs=False)
        self.src, self.cls = src, cls
        self.line_starts = [0] + [i + 1 for i, c in enumerate(src) if c == '\n']
        self.depth, self.open_at, self.ranges = 0, None, []

    def _offset(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get('class') or '').split()
        start = self._offset()
        if tag in VOID:
            if self.open_at is None and self.cls in classes:
                self.ranges.append((start, start + len(self.get_starttag_text())))
            return
        self.depth += 1
        if self.open_at is None and self.cls in classes:
            self.open_at = (start, self.depth)

    def handle_startendtag(self, tag, attrs):
        classes = (dict(attrs).get('class') or '').split()
        if self.open_at is None and self.cls in classes:
            start = self._offset()
            self.ranges.append((start, start + len(self.get_starttag_text())))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.open_at and self.depth == self.open_at[1]:
            end = self.src.index('>', self._offset()) + 1
            self.ranges.append((self.open_at[0], end))
            self.open_at = None
        self.depth -= 1


def strip_class(src, cls):
    """Remove elements with class `cls`; drop lines they leave empty."""
    parser = _Ranges(src, cls)
    parser.feed(src)
    out, pos = [], 0
    for start, end in sorted(parser.ranges):
        line_start = src.rfind('\n', 0, start) + 1
        line_end = src.find('\n', end)
        line_end = len(src) if line_end == -1 else line_end
        if not src[line_start:start].strip() and not src[end:line_end].strip():
            start, end = line_start, min(line_end + 1, len(src))   # whole line was just this element
        out.append(src[pos:start])
        pos = end
    out.append(src[pos:])
    return ''.join(out)


def localize_attrs(src, lang):
    """attr="English" data-ja-attr="日本語" -> keep the value for `lang`."""
    pattern = re.compile(r'([a-z][a-z-]*)="([^"]*)"\s+data-ja-\1="([^"]*)"')
    return pattern.sub(lambda m: f'{m.group(1)}="{m.group(3) if lang == "ja" else m.group(2)}"', src)


def build():
    template = open(TEMPLATE, encoding='utf-8').read()
    for lang, page in PAGES.items():
        html = strip_class(template, 'lang-ja' if lang == 'en' else 'lang-en')
        html = localize_attrs(html, lang)
        # mark the current language in the switcher
        html = html.replace(f'hreflang="{lang}" lang="{lang}">', f'hreflang="{lang}" lang="{lang}" aria-current="page">', 1)
        values = {
            'LANG': lang, 'TITLE': page['title'], 'DESCRIPTION': page['description'], 'URL': page['url'],
            'OG_TITLE': page['og_title'], 'OG_DESCRIPTION': page['og_description'],
            'OG_LOCALE': page['og_locale'], 'OG_LOCALE_ALT': page['og_locale_alt'],
            'JSONLD': jsonld(lang, page), 'HEAD_SCRIPT': page['head_script'],
        }
        for key, value in values.items():
            html = html.replace('{{' + key + '}}', value)
        leftover = re.findall(r'\{\{[A-Z_]+\}\}', html)
        assert not leftover, f'unfilled placeholders: {leftover}'
        html = html.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n<!-- Generated by _src/build_pages.py from _src/index.template.html; edit the template, not this file. -->\n', 1)
        path = os.path.join(ROOT, page['out'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('wrote', page['out'])

    today = datetime.date.today().isoformat()
    alternates = ''.join(
        f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>'
        for h, u in (('en', f'{SITE}/'), ('ja', f'{SITE}/ja/'), ('x-default', f'{SITE}/')))
    urls = ''.join(f'\n  <url>\n    <loc>{p["url"]}</loc>\n    <lastmod>{today}</lastmod>{alternates}\n  </url>'
                   for p in PAGES.values())
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
               f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}\n</urlset>\n')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print('wrote sitemap.xml')


if __name__ == '__main__':
    build()
