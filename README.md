# ttm-telegram

MCP server đọc tin nhắn **nhóm Telegram** bằng **tài khoản Telegram của chính bạn**. Chạy trên máy bạn. Dữ liệu đi thẳng từ máy bạn tới Telegram, không qua dịch vụ nào khác.

## Công cụ (3 tool)

| Tool | Làm gì |
|---|---|
| `list_groups` | Liệt kê nhóm được phép đọc (theo `ALLOWED_GROUP_IDS`) |
| `get_messages` | Đọc tin nhắn chữ của một nhóm trong khoảng ngày (`YYYY-MM-DD`), tối đa 1000 tin |
| `search_messages` | Tìm tin nhắn trong nhóm theo từ khóa, tối đa 200 kết quả |

## Trước khi cài

1. Lấy **API id** và **API hash** tại <https://my.telegram.org>, đăng nhập bằng số điện thoại Telegram của bạn, mục *API development tools*.

## Cài nhanh (khuyến nghị, không cần Python)

**macOS / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/toantranmei/ttm-telegram/main/install.sh | sh
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/toantranmei/ttm-telegram/main/install.ps1 | iex
```

### Bước 1 – Đăng nhập một lần để tạo session

Trên macOS/Linux:
```bash
TELEGRAM_API_ID=<id> TELEGRAM_API_HASH=<hash> "$HOME/.local/bin/ttm-telegram" login
```

Trên Windows:
```powershell
$env:TELEGRAM_API_ID="<id>"; $env:TELEGRAM_API_HASH="<hash>"; & "$env:LOCALAPPDATA\ttm\bin\ttm-telegram.exe" login
```

Lần đầu Telegram sẽ gửi mã xác nhận tới bạn. Sau khi đăng nhập, lệnh in ra danh sách nhóm kèm `Group ID`. Ghi lại ID các nhóm bạn muốn cho phép đọc.

Session lưu tại `~/.ttm-telegram/session.session` (trên Windows là `%USERPROFILE%\.ttm-telegram\`). **Đây là chìa khóa tài khoản của bạn: không chia sẻ, không commit.**

### Bước 2 – Đăng ký với Claude Code

```bash
claude mcp add ttm-telegram \
  -e TELEGRAM_API_ID=<id> \
  -e TELEGRAM_API_HASH=<hash> \
  -e ALLOWED_GROUP_IDS=-1001234567890 \
  -- "$HOME/.local/bin/ttm-telegram"
```

## Claude Desktop (không dùng terminal)

Tải file `ttm-telegram-*.mcpb` mới nhất ở trang [Releases](https://github.com/toantranmei/ttm-telegram/releases), nhấp đúp để cài, rồi điền **API id**, **API hash** và **group_id được phép đọc** trong giao diện. Bước đăng nhập một lần (Bước 1 ở trên) vẫn cần chạy trong terminal một lần.

## Cài bằng Python (tùy chọn)

Nếu bạn đã có [`uv`](https://docs.astral.sh/uv/): `uvx ttm-telegram` (sau khi có gói PyPI). Bước đăng nhập: `uvx --from ttm-telegram ttm-telegram login`.

## Biến môi trường

| Biến | Bắt buộc | Mặc định | Mô tả |
|---|---|---|---|
| `TELEGRAM_API_ID` | có | — | API id từ my.telegram.org |
| `TELEGRAM_API_HASH` | có | — | API hash từ my.telegram.org |
| `TELEGRAM_SESSION` | không | `~/.ttm-telegram/session` | Đường dẫn file session (không kèm `.session`) |
| `ALLOWED_GROUP_IDS` | không | *(trống)* | `group_id` được đọc, cách nhau dấu phẩy, hoặc `ALL`. **Trống = không đọc nhóm nào.** |
| `TELEGRAM_TZ` | không | `Asia/Ho_Chi_Minh` | Múi giờ để tính khoảng ngày và hiển thị thời gian |

## Quyền riêng tư và trách nhiệm

- Server chỉ đọc các nhóm nằm trong `ALLOWED_GROUP_IDS`. Mặc định không đọc nhóm nào.
- Tin nhắn được trả về cho AI client bạn đang dùng. Cân nhắc trước khi cho AI đọc nhóm có thông tin nhạy cảm.
- Tài khoản Telegram là của bạn. Bạn tự chịu trách nhiệm tuân thủ điều khoản của Telegram và quyền riêng tư của thành viên nhóm.
- Không có chế độ http, không mở cổng mạng.

## Phát triển

```bash
git clone https://github.com/toantranmei/ttm-telegram && cd ttm-telegram
uv run --with-editable . ttm-telegram            # chạy stdio
packaging/build.sh ttm-telegram darwin-arm64     # dựng binary + archive trong dist/release/
```

Phát hành: đẩy tag `v*` để GitHub Actions dựng binary cho 4 nền tảng, đóng gói `.mcpb` và tạo Release.

## Giấy phép

MIT. Xem [LICENSE](LICENSE).
