#!/usr/bin/env python3
"""Regenerate download content and installer default from the release manifest.

Run from any directory: python3 scripts/gen_download.py
No network or third-party dependencies; output remains plain static HTML.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
START, END = '<!-- DOWNLOAD:START -->', '<!-- DOWNLOAD:END -->'


def code(value):
    return '<pre class="term"><code>' + html.escape(value.strip()) + '</code></pre>'


def generate():
    release = json.loads((SITE / 'download/release.json').read_text())
    version = release['version']
    if not re.fullmatch(r'[0-9][0-9A-Za-z._+-]*', version):
        raise ValueError('Invalid release version')
    assets = release['assets']
    names = set()
    for asset in assets:
        if asset['file'] in names or not re.fullmatch(r'[a-f0-9]{64}', asset['sha256']):
            raise ValueError('Duplicate asset or malformed checksum')
        if not isinstance(asset['bytes'], int) or asset['bytes'] <= 0:
            raise ValueError('Invalid asset byte count')
        if not asset['url'].startswith(release['repo'] + '/releases/download/' + release['tag'] + '/'):
            raise ValueError('Asset URL does not match release')
        names.add(asset['file'])
    installer = SITE / 'install.sh'
    script, count = re.subn(r"^DEFAULT_VERSION='[^']*'$", f"DEFAULT_VERSION='{version}'", installer.read_text(), flags=re.M)
    if count != 1:
        raise ValueError('Installer default version marker is missing or duplicated')
    installer.write_text(script)
    h = html.escape
    content = f'''<section id="release"><h2>Current release</h2>
<p><strong>{h(version)}</strong> · <time datetime="{h(release['date'])}">{h(release['date'])}</time> · {h(release['channel'])} channel</p>
<p><a href="{h(release['repo'])}/releases/tag/{h(release['tag'])}">Release notes</a> · <a href="{h(release['checksums'])}">checksums.txt</a> · <a href="/download/release.json">Release manifest</a></p>
<p>These are public GitHub release archives. Sizes below are exact compressed bytes. SHA-256 checksums detect corruption; this release does not provide a separate signature verification step.</p>
<div class="table-scroll download-assets" tabindex="0" role="region" aria-label="CLI release assets"><table class="table"><thead><tr><th scope="col">OS</th><th scope="col">Architecture</th><th scope="col">Size (bytes)</th><th scope="col">SHA-256</th><th scope="col">Download</th></tr></thead><tbody>'''
    for a in assets:
        os_name = {'darwin': 'macOS', 'linux': 'Linux', 'windows': 'Windows'}.get(a['os'], a['os'])
        arch = {'amd64': 'amd64 (x86-64)', 'arm64': 'arm64 (AArch64)'}.get(a['arch'], a['arch'])
        content += f'<tr><td>{h(os_name)}</td><td>{h(arch)}</td><td>{a["bytes"]:,}</td><td><code class="checksum">{h(a["sha256"])}</code></td><td><a href="{h(a["url"])}" data-event="download_click">{h(a["file"])}</a></td></tr>\n'
    content += '</tbody></table></div></section>\n<section id="manual"><h2>Manual installation first</h2><p>Choose your OS and processor in the table. The commands below use actual archives and their manifest checksums. Stop if the computed checksum differs. On macOS or Linux, install only after verification succeeds, then add <code>$HOME/.local/bin</code> to your shell’s PATH.</p>'
    for os_name, label, check in [('darwin', 'macOS', 'shasum -a 256'), ('linux', 'Linux', 'sha256sum')]:
        for a in [x for x in assets if x['os'] == os_name]:
            content += f'<h3>{label} · {h(a["arch"])}</h3>'
            commands = f'''(
  set -eu
  curl -fsSL '{a['url']}' -o '{a['file']}'
  printf '%s  %s\\n' '{a['sha256']}' '{a['file']}' | {check} -c -
  tar -xzf '{a['file']}' inferra
  mkdir -p "$HOME/.local/bin"
  install -m 755 inferra "$HOME/.local/bin/inferra"
  "$HOME/.local/bin/inferra" version
)'''
            content += code(commands)
    content += '<p>For the current shell on macOS or Linux:</p>' + code('export PATH="$HOME/.local/bin:$PATH"')
    for a in [x for x in assets if x['os'] == 'windows']:
        content += f'<h3>Windows · {h(a["arch"])}</h3><p>Run in PowerShell. Add the installation directory printed below to your user PATH for future terminals.</p>'
        content += code(f'''$ErrorActionPreference = 'Stop'
Invoke-WebRequest -Uri '{a['url']}' -OutFile '{a['file']}'
$actual = (Get-FileHash -Algorithm SHA256 '{a['file']}').Hash
if ($actual -ne '{a['sha256']}') {{ throw 'SHA-256 mismatch; stop installation' }}
$dest = Join-Path $env:LOCALAPPDATA 'Inferra\\bin'
$unpack = Join-Path ([System.IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString())
try {{
  Expand-Archive -Path '{a['file']}' -DestinationPath $unpack
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Copy-Item (Join-Path $unpack 'inferra.exe') (Join-Path $dest 'inferra.exe') -Force
}} finally {{
  if (Test-Path $unpack) {{ Remove-Item $unpack -Recurse -Force }}
}}
$env:Path = "$dest;$env:Path"
inferra version
Write-Output "Add this directory to your user PATH: $dest"''')
    content += '</section><section id="installer"><h2>Optional shell installer</h2><p>For macOS and Linux, this downloads the detected archive and checksums.txt from the pinned GitHub release, verifies SHA-256, and installs without sudo. It requires curl, tar and either sha256sum or shasum. The default destination is <code>$HOME/.local/bin</code>; override it with <code>INFERRA_INSTALL_DIR</code>.</p>'
    content += code('curl -fsSL https://inferralab.com/install.sh | sh')
    content += '<p>Read the full script below, or <a href="/install.sh">download it for inspection</a>. The default is the manifest’s preview version, not GitHub’s “latest” release.</p><h3>The complete installer</h3><!-- LAUNCH: production API host -->'
    content += code(script)
    content += '<h3>Pin a version or destination</h3>' + code(f'''curl -fsSL https://inferralab.com/install.sh -o install.sh
INFERRA_VERSION={version} INFERRA_INSTALL_DIR="$HOME/.local/bin" sh install.sh''')
    content += '<p><code>INFERRA_VERSION</code> accepts a version with or without the leading <code>v</code>. Use an existing release with matching archives and checksums. An unavailable version, missing checksum tool or checksum mismatch stops installation.</p></section>'
    content += '<section id="update"><h2>Update and sign in</h2><p>Repeat the manual installation for the desired release, or rerun the installer. It replaces only the executable. Version pinning stays explicit; there is no automatic “latest” lookup.</p>' + code('inferra version\ninferra login --api https://api.dev.inferralab.com') + '<!-- LAUNCH: production API host --><p>During preview, always pass this API address at login. The current CLI’s built-in default is incorrect. Continue with <a href="/setup">the setup guide</a>.</p></section>'
    content += '<section id="uninstall"><h2>Uninstall the local CLI</h2><p>Log out before removing the binary. For the default macOS/Linux destination:</p>' + code('inferra logout\nrm -f "$HOME/.local/bin/inferra"')
    content += '<p>For the Windows destination used above:</p>' + code("inferra logout\nRemove-Item (Join-Path $env:LOCALAPPDATA 'Inferra\\bin\\inferra.exe')")
    content += '<p>If you chose another install directory, remove its inferra executable instead. Remove the PATH entry you added if the directory is no longer needed. This does not delete deployed apps, the GitHub App installation, or your platform account. Logout clears the saved local login; revoke the personal token in Settings → Tokens if it should no longer work anywhere.</p></section>'
    path = SITE / 'download/index.html'
    page = path.read_text()
    if page.count(START) != 1 or page.count(END) != 1:
        raise ValueError('Download markers must each appear once')
    before, tail = page.split(START)
    _, after = tail.split(END)
    path.write_text(before + START + '\n' + content + '\n' + END + after)
    print(f'Generated {len(assets)} asset rows and all install examples for {version}.')


if __name__ == '__main__':
    generate()
