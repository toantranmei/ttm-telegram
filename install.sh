#!/usr/bin/env bash
# Cài ttm-telegram (binary đã build sẵn) vào ~/.local/bin. Không cần Python hay uv.
#   curl -fsSL https://raw.githubusercontent.com/toantranmei/ttm-telegram/main/install.sh | sh
# Biến tùy chọn: TTM_VERSION (mặc định bản mới nhất), TTM_INSTALL_DIR, TTM_BASE_URL (dùng để thử cục bộ).
set -euo pipefail

NAME="ttm-telegram"
REPO="toantranmei/ttm-telegram"
INSTALL_DIR="${TTM_INSTALL_DIR:-$HOME/.local/bin}"
if [ -n "${TTM_BASE_URL:-}" ]; then BASE="$TTM_BASE_URL"
elif [ -n "${TTM_VERSION:-}" ]; then BASE="https://github.com/$REPO/releases/download/$TTM_VERSION"
else BASE="https://github.com/$REPO/releases/latest/download"; fi

os="$(uname -s)"; arch="$(uname -m)"
case "$os" in
  Darwin) os_id="darwin" ;;
  Linux)  os_id="linux" ;;
  *) echo "Hệ điều hành chưa hỗ trợ: $os. Trên Windows dùng install.ps1." >&2; exit 1 ;;
esac
case "$arch" in
  arm64|aarch64) arch_id="arm64" ;;
  x86_64|amd64)  arch_id="x64" ;;
  *) echo "Kiến trúc chưa hỗ trợ: $arch" >&2; exit 1 ;;
esac

target="$os_id-$arch_id"
archive="$NAME-$target.tar.gz"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

echo "Tải $archive ..."
curl -fsSL "$BASE/$archive" -o "$tmp/$archive"
curl -fsSL "$BASE/$archive.sha256" -o "$tmp/$archive.sha256"

expected="$(tr -d '[:space:]' < "$tmp/$archive.sha256")"
if command -v shasum >/dev/null; then actual="$(shasum -a 256 "$tmp/$archive" | awk '{print $1}')"
else actual="$(sha256sum "$tmp/$archive" | awk '{print $1}')"; fi
if [ "$expected" != "$actual" ]; then
  echo "Sai checksum. Dừng cài đặt." >&2; exit 1
fi

tar -xzf "$tmp/$archive" -C "$tmp"
mkdir -p "$INSTALL_DIR"
install -m 0755 "$tmp/$NAME" "$INSTALL_DIR/$NAME"

echo ""
echo "Đã cài: $INSTALL_DIR/$NAME"
case ":$PATH:" in *":$INSTALL_DIR:"*) ;; *) echo "Lưu ý: $INSTALL_DIR chưa có trong PATH. Thêm vào ~/.zshrc hoặc ~/.bashrc:  export PATH=\"$INSTALL_DIR:\$PATH\"";; esac
echo ""
echo "Chạy bước đăng nhập một lần trước: lệnh `ttm-telegram login` (xem README)."
echo ""
echo "Đăng ký với Claude Code (thay giá trị trong <>):"
cat <<'CMD'
# 1) Đăng nhập một lần để tạo session (xem group_id):
TELEGRAM_API_ID=<id> TELEGRAM_API_HASH=<hash> "$HOME/.local/bin/ttm-telegram" login
# 2) Đăng ký với Claude Code:
claude mcp add ttm-telegram \
  -e TELEGRAM_API_ID=<id> \
  -e TELEGRAM_API_HASH=<hash> \
  -e ALLOWED_GROUP_IDS=<group_id> \
  -- "$HOME/.local/bin/ttm-telegram"
CMD
echo ""
echo "Claude Desktop: tải bundle .mcpb ở trang Releases và mở file, rồi điền cấu hình trong giao diện."
