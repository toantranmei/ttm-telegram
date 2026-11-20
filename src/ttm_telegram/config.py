"""Cấu hình đọc từ biến môi trường. Không có giá trị bí mật nào trong mã nguồn."""

import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

DEFAULT_SESSION_DIR = Path.home() / ".ttm-telegram"


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Thiếu biến môi trường {name}. Xem README: lấy API id/hash tại https://my.telegram.org."
        )
    return value


API_ID = int(_required("TELEGRAM_API_ID"))
API_HASH = _required("TELEGRAM_API_HASH")

# Đường dẫn file session (không có đuôi .session). Mặc định nằm trong thư mục cá nhân, không nằm trong repo.
SESSION = os.getenv("TELEGRAM_SESSION", str(DEFAULT_SESSION_DIR / "session"))

# Nhóm được phép đọc: danh sách ID cách nhau dấu phẩy, hoặc ALL. Để trống = không cho đọc nhóm nào.
ALLOWED_GROUP_IDS = os.getenv("ALLOWED_GROUP_IDS", "")
ALLOW_ALL_GROUPS = ALLOWED_GROUP_IDS.strip().upper() == "ALL"
ALLOWED_GROUPS = (
    set()
    if ALLOW_ALL_GROUPS
    else {int(x.strip()) for x in ALLOWED_GROUP_IDS.split(",") if x.strip()}
)

# Múi giờ dùng để hiển thị và tính khoảng ngày. Mặc định Việt Nam.
TZ = ZoneInfo(os.getenv("TELEGRAM_TZ", "Asia/Ho_Chi_Minh"))


def ensure_session_dir() -> None:
    Path(SESSION).expanduser().parent.mkdir(parents=True, exist_ok=True)
