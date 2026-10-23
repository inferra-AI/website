"""Offline checks for the public configuration and billing promises."""
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class CustomerJourney(unittest.TestCase):
    def test_no_retired_configuration_in_instructions(self):
        for path in [*SITE.rglob('*.html'), *SITE.glob('llms*.txt'), *SITE.glob('setup/*.yaml')]:
            with self.subTest(page=str(path.relative_to(SITE))):
                text = path.read_text()
                # The old reference/download URLs remain valid bookmarks.
                text = re.sub(r'(?:href|content)=["\'][^"\']*["\']', '', text)
                text = re.sub(r'https://inferralab.com/(?:docs/org-yaml/|setup/org[^\s]*)', '', text)
                self.assertNotRegex(text, r'(?i)org\.yaml|\.inferra/(?:main|feature|<branch>)\.yaml|version: [12]\b|writes (?:a supported )?v1|generates (?:the )?version-1|run\.process: worker')

    def test_no_retired_inferra_billing(self):
        for path in [*SITE.rglob('*.html'), *SITE.glob('llms*.txt'), SITE / 'calculator.js']:
            with self.subTest(page=str(path.relative_to(SITE))):
                text = path.read_text()
                self.assertNotRegex(text, r'(?i)prepaid|16\.19|1\.78|0\.104|first \$5|\$5 of usage free|3.day grace|apps pause after 3 days|data (?:is )?kept (?:for )?7 days|no plans|Wallet → Redeem|Preview databases start independently|independent bound services|Credits left|Real config from the public demo|Bring your own Docker image is available|Each branch has its own Postgres')

    def test_setup_explains_v3_account_service_order(self):
        text = (SITE / 'setup/index.html').read_text()
        for term in ['.inferra/repo.yaml', '.inferra/app.yaml', 'version: 3', 'account.yaml', 'services/orders.yaml', 'private', 'service change first', 'ORDERS_URL']:
            self.assertIn(term, text)

    def test_billing_has_locked_terms(self):
        text = (SITE / 'docs/billing/index.html').read_text()
        for term in ['$15', '14 days', 'card', '$25', 'mid-month', 'month-end', '$100', 'once a day', '3 months', '00:00 UTC', '30 days', 'support@inferralab.com']:
            self.assertIn(term, text)

    def test_api_matches_cli_default(self):
        for path in SITE.rglob('*'):
            if path.suffix not in ('.html', '.txt', '.js', '.sh', '.json'): continue
            with self.subTest(page=str(path.relative_to(SITE))):
                hosts = re.findall(r'https://(api\.[a-z.]*[a-z])', path.read_text())
                self.assertTrue(all(host == 'api.inferralab.com' for host in hosts), hosts)

    def test_terms_and_structured_data(self):
        self.assertTrue((SITE / 'terms/index.html').is_file())
        for path in SITE.rglob('*.html'):
            for payload in re.findall(r'<script type="application/ld\+json">(.*?)</script>', path.read_text(), re.S):
                json.loads(payload)

    def test_local_links_and_copy_buttons(self):
        class Page(HTMLParser):
            def __init__(self, source):
                super().__init__()
                self.ids, self.links, self.copies = [], [], []
                self.feed(source)

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.append(attrs['id'])
                for key in ('href', 'src'):
                    if key in attrs:
                        self.links.append(attrs[key])
                if 'data-copy' in attrs:
                    self.copies.append(attrs['data-copy'])

        pages = {path: Page(path.read_text()) for path in SITE.rglob('*.html')}
        count = 0
        for path, page in pages.items():
            with self.subTest(page=str(path.relative_to(SITE))):
                self.assertEqual(len(page.ids), len(set(page.ids)), 'Duplicate IDs')
                for target in page.copies:
                    self.assertIn(target, page.ids, 'Copy button has no source')
                for href in page.links:
                    url = urlsplit(urljoin('/' + str(path.relative_to(SITE)), href))
                    if url.scheme or url.netloc:
                        continue
                    target = SITE / unquote(url.path).lstrip('/')
                    if target.is_dir():
                        target /= 'index.html'
                    self.assertTrue(target.is_file(), href)
                    count += 1
                    if url.fragment and target in pages:
                        self.assertIn(unquote(url.fragment), pages[target].ids, href)
        print(f'Local references: {len(pages)} pages, {count} links/assets checked')

    def test_html_nesting(self):
        class Nesting(HTMLParser):
            void = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img',
                    'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

            def __init__(self, source):
                super().__init__()
                self.stack, self.errors = [], []
                self.feed(source)

            def handle_starttag(self, tag, attrs):
                if tag not in self.void:
                    self.stack.append(tag)

            def handle_startendtag(self, tag, attrs):
                pass

            def handle_endtag(self, tag):
                if tag in self.void:
                    return
                if not self.stack or self.stack[-1] != tag:
                    self.errors.append((self.getpos(), tag, self.stack[-3:]))
                else:
                    self.stack.pop()

        for path in SITE.rglob('*.html'):
            with self.subTest(page=str(path.relative_to(SITE))):
                parsed = Nesting(path.read_text())
                self.assertEqual(parsed.errors, [])
                self.assertEqual(parsed.stack, [])

    def test_calculator_paid_total(self):
        # Execute the actual browser script with a minimal DOM; inspect the values
        # customers see. $40 usage => $40 Paid total; $18 usage => $25 minimum.
        subprocess.run(['node', str(ROOT / 'tests/calculator.test.cjs')], check=True, cwd=ROOT)

if __name__ == '__main__':
    unittest.main()
