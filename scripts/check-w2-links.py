#!/usr/bin/env python3
"""Check W2 local hrefs, fragments, assets, noindex and shared shell offline."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import re

root = Path(__file__).resolve().parents[1] / 'site'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links = []; self.ids = set(); self.noindex = False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'meta' and a.get('name') == 'robots':
            self.noindex = 'noindex' in a.get('content', '')
        for key in ('href', 'src'):
            if key in a: self.links.append((key, a[key]))

def block(text, tag):
    return re.search(fr'<{tag}\b.*?</{tag}>', text, re.S)[0]

home = (root / 'index.html').read_text()
errors = []
for name in ('ai', 'start', 'templates', 'agencies'):
    text = (root / name / 'index.html').read_text(); page = Page(text)
    count = 0
    for kind, href in page.links:
        u = urlsplit(urljoin('/' + name + '/', href))
        if u.scheme or u.netloc: continue
        target = (root / unquote(u.path).lstrip('/')).resolve()
        if target.is_dir(): target /= 'index.html'
        count += 1
        if not target.is_relative_to(root) or not target.is_file():
            errors.append(f'{name}: missing {kind} {href}'); continue
        if u.fragment and target.suffix == '.html' and unquote(u.fragment) not in Page(target.read_text()).ids:
            errors.append(f'{name}: missing fragment {href}')
    assert page.noindex, name
    assert all(block(text, tag) == block(home, tag) for tag in ('header', 'footer')), name
    assert all(f'href="/{css}.css"' in text for css in ('styles', 'light', 'v5', 'tpl')), name
    assert 'src="/v5.js"' in text, name
    print(f'{name}: {count} local href/src references checked; noindex and v5 shell OK')
for error in errors: print(error)
print(f'Broken local references: {len(errors)}')
raise SystemExit(bool(errors))
