#!/usr/bin/env bash
# Đóng gói binary cho nền tảng hiện tại và tạo archive + sha256 trong dist/release/.
#   packaging/build.sh <tên-binary> <os-arch, ví dụ darwin-arm64>
set -euo pipefail

name="${1:?tên binary}"
target="${2:?os-arch}"
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

uv run --quiet --with "pyinstaller==6.*" --with "mcp==2.3.0" --with-editable . \
  pyinstaller --noconfirm --onefile --clean --name "$name" \
  --paths src packaging/entry.py

rel="dist/release"
rm -rf "$rel" && mkdir -p "$rel"
exe="dist/$name"
[[ "$target" == windows-* ]] && exe="dist/$name.exe"

if [[ "$target" == windows-* ]]; then
  archive="$rel/$name-$target.zip"
  (cd dist && powershell -NoProfile -Command "Compress-Archive -Path '$name.exe' -DestinationPath '../$archive'")
else
  archive="$rel/$name-$target.tar.gz"
  tar -C dist -czf "$archive" "$(basename "$exe")"
fi

if command -v shasum >/dev/null; then shasum -a 256 "$archive" | awk '{print $1}' > "$archive.sha256"
else sha256sum "$archive" | awk '{print $1}' > "$archive.sha256"; fi
echo "built $archive"
