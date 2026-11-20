#!/usr/bin/env bash
# Đóng gói binary cho một nền tảng và tạo archive + sha256 trong dist/release/.
#   packaging/build.sh <tên-binary> <os-arch>
#   os-arch: darwin-arm64 | darwin-x64 | linux-x64 | linux-arm64 | windows-x64
# Linux build trong container python:3.12-slim-bullseye (Debian 11, glibc 2.31; cần Docker).
set -euo pipefail

name="${1:?tên binary}"
target="${2:?os-arch}"
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if [[ "$target" == linux-* ]]; then
  case "$target" in
    linux-x64)   image="python:3.12-slim-bullseye" ;;
    linux-arm64) image="python:3.12-slim-bullseye" ;;
  esac
  docker run --rm -e NAME="$name" -e HOST_UID="$(id -u)" -e HOST_GID="$(id -g)" \
    -v "$root:/src" -w /src "$image" bash packaging/linux-inside.sh
else
  uv run --quiet --python 3.12 --with "pyinstaller==6.*" --with "mcp==2.3.0" --with-editable . \
    pyinstaller --noconfirm --onefile --clean --name "$name" \
    --paths src packaging/entry.py
fi

rel="dist/release"
rm -rf "$rel" && mkdir -p "$rel"

if [[ "$target" == windows-* ]]; then
  archive="$rel/$name-$target.zip"
  (cd dist && powershell -NoProfile -Command "Compress-Archive -Path '$name.exe' -DestinationPath '../$archive'")
else
  archive="$rel/$name-$target.tar.gz"
  tar -C dist -czf "$archive" "$name"
fi

if command -v shasum >/dev/null; then shasum -a 256 "$archive" | awk '{print $1}' > "$archive.sha256"
else sha256sum "$archive" | awk '{print $1}' > "$archive.sha256"; fi
echo "built $archive"
