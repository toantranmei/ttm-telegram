"""Điểm vào cho binary (PyInstaller).

  ttm-telegram            chạy MCP server qua stdio (AI client gọi lệnh này)
  ttm-telegram login      đăng nhập Telegram một lần để tạo session và liệt kê group_id
"""

import sys

from ttm_telegram.login import main as login
from ttm_telegram.server import main as serve

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "login":
        login()
    else:
        serve()
