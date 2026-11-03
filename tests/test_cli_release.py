"""Release checks require gh, GitHub access, and no write permissions.

Run: python3 -m unittest discover -s tests -p test_cli_release.py -v
"""
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CLIRelease(unittest.TestCase):
    def test_owner_approved_release(self):
        release = json.loads((ROOT / 'site/download/release.json').read_text())
        self.assertEqual(release['version'], '0.4.0-rc.97')

    def test_installer_and_manifest_match_published_release(self):
        release = json.loads((ROOT / 'site/download/release.json').read_text())
        defaults = re.findall(r"^DEFAULT_VERSION='([^']+)'$",
                              (ROOT / 'site/install.sh').read_text(), re.M)
        self.assertEqual(defaults, [release['version']])
        self.assertEqual(release['tag'], 'v' + release['version'])
        self.assertEqual(release['repo'], 'https://github.com/inferra-AI/cli')
        published = json.loads(subprocess.check_output([
            'gh', 'release', 'view', release['tag'], '-R', 'inferra-AI/cli',
            '--json', 'assets,isDraft,publishedAt,tagName'], text=True))
        self.assertFalse(published['isDraft'])
        self.assertTrue(published['publishedAt'])
        self.assertEqual(published['tagName'], release['tag'])
        self.assertEqual(release['date'], published['publishedAt'][:10])
        checksums = subprocess.check_output([
            'gh', 'release', 'download', release['tag'], '-R', 'inferra-AI/cli',
            '-p', 'checksums.txt', '-O', '-'], text=True)
        sums = dict(line.split()[::-1] for line in checksums.splitlines())
        assets = {asset['name']: asset for asset in published['assets']}
        base = release['repo'] + '/releases/download/' + release['tag'] + '/'
        self.assertEqual(release['checksums'], base + 'checksums.txt')
        self.assertEqual(len(release['assets']), 6)
        self.assertEqual(len({a['file'] for a in release['assets']}), 6)
        for asset in release['assets']:
            with self.subTest(asset=asset['file']):
                extension = 'zip' if asset['os'] == 'windows' else 'tar.gz'
                self.assertEqual(asset['file'],
                                 f"inferra_{release['version']}_{asset['os']}_{asset['arch']}.{extension}")
                actual = assets[asset['file']]
                self.assertEqual(asset['url'], actual['url'])
                self.assertEqual(asset['bytes'], actual['size'])
                self.assertEqual(asset['sha256'], sums[asset['file']])


if __name__ == '__main__':
    unittest.main()
