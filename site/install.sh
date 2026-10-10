#!/bin/sh
set -eu

# Generated default from site/download/release.json; prereleases are not latest.
DEFAULT_VERSION='0.4.0-rc.17'
version=${INFERRA_VERSION:-$DEFAULT_VERSION}
version=${version#v}
case "$version" in
  ''|*[!0-9A-Za-z._+-]*|[!0-9]*) printf '%s\n' 'Invalid INFERRA_VERSION.' >&2; exit 1 ;;
esac
case $(uname -s) in
  Linux) os=linux ;;
  Darwin) os=darwin ;;
  *) printf '%s\n' 'Supported systems: Linux and macOS. Download Windows archives from https://inferralab.com/download.' >&2; exit 1 ;;
esac
case $(uname -m) in
  x86_64|amd64) arch=amd64 ;;
  arm64|aarch64) arch=arm64 ;;
  *) printf '%s\n' 'Unsupported architecture; expected amd64 or arm64.' >&2; exit 1 ;;
esac
for tool in curl tar mktemp awk; do
  command -v "$tool" >/dev/null 2>&1 || { printf 'Required tool missing: %s\n' "$tool" >&2; exit 1; }
done
if command -v sha256sum >/dev/null 2>&1; then
  checksum=sha256sum
elif command -v shasum >/dev/null 2>&1; then
  checksum=shasum
else
  printf '%s\n' 'SHA-256 verification requires sha256sum or shasum; nothing installed.' >&2
  exit 1
fi
install_dir=${INFERRA_INSTALL_DIR:-"$HOME/.local/bin"}
case "$install_dir" in /*) ;; *) install_dir="$PWD/$install_dir" ;; esac
archive="inferra_${version}_${os}_${arch}.tar.gz"
release="https://github.com/inferra-AI/cli/releases/download/v${version}"
work=$(mktemp -d)
trap 'rm -rf "$work"' 0
trap 'exit 1' HUP INT TERM
curl -fsSL "$release/$archive" -o "$work/$archive"
curl -fsSL "$release/checksums.txt" -o "$work/checksums.txt"
expected=$(awk -v name="$archive" '$2 == name || $2 == "*" name { print $1; count++ } END { if (count != 1) exit 1 }' "$work/checksums.txt") || {
  printf '%s\n' 'Archive is missing or duplicated in checksums.txt; nothing installed.' >&2; exit 1;
}
case "$expected" in ''|*[!0-9a-fA-F]*) printf '%s\n' 'Invalid SHA-256 checksum.' >&2; exit 1 ;; esac
[ "${#expected}" -eq 64 ] || { printf '%s\n' 'Invalid SHA-256 checksum length.' >&2; exit 1; }
if [ "$checksum" = sha256sum ]; then
  actual=$(sha256sum "$work/$archive" | awk '{print $1}')
else
  actual=$(shasum -a 256 "$work/$archive" | awk '{print $1}')
fi
[ "$actual" = "$expected" ] || { printf '%s\n' 'SHA-256 mismatch; nothing installed.' >&2; exit 1; }
# Extract only the binary from the verified archive.
tar -xzf "$work/$archive" -C "$work" inferra
[ -f "$work/inferra" ] && [ ! -L "$work/inferra" ] || { printf '%s\n' 'Archive has no regular inferra binary.' >&2; exit 1; }
mkdir -p "$install_dir"
# Stage beside the destination so a failed copy leaves the current CLI intact.
staged=$(mktemp "$install_dir/.inferra.XXXXXXXX")
trap 'rm -rf "$work"; rm -f "$staged"' 0
cp "$work/inferra" "$staged"
chmod 755 "$staged"
mv -f "$staged" "$install_dir/inferra"
printf 'Installed Inferra %s to %s/inferra\n' "$version" "$install_dir"
printf 'Add this directory to PATH in your shell profile: %s\n' "$install_dir"
# LAUNCH: production API host
printf '%s\n' 'Next: inferra login --api https://api.dev.inferralab.com'
