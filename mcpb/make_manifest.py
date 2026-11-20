"""Sinh manifest.json cho một nền tảng: python3 make_manifest.py <platform> <bin> <version>."""
import json, sys

PARAMS = {'display': 'Telegram (ttm-telegram)', 'desc': 'MCP server đọc tin nhắn nhóm Telegram bằng tài khoản của chính bạn (chạy trên máy bạn)', 'long': 'Chạy trên máy bạn. Dữ liệu đi thẳng từ máy bạn tới Telegram. Cần đăng nhập Telegram một lần để tạo session.', 'user_config': {'api_id': {'type': 'string', 'title': 'Telegram API id', 'description': 'Lấy tại https://my.telegram.org', 'required': True}, 'api_hash': {'type': 'string', 'title': 'Telegram API hash', 'description': 'Lấy tại https://my.telegram.org', 'sensitive': True, 'required': True}, 'allowed_group_ids': {'type': 'string', 'title': 'group_id được phép đọc', 'description': 'Cách nhau dấu phẩy, hoặc ALL. Để trống = không đọc nhóm nào.', 'required': False}}, 'env': {'TELEGRAM_API_ID': '${user_config.api_id}', 'TELEGRAM_API_HASH': '${user_config.api_hash}', 'ALLOWED_GROUP_IDS': '${user_config.allowed_group_ids}'}}

platform, bin_name, version = sys.argv[1], sys.argv[2], sys.argv[3]
cmd = "${__dirname}/server/" + bin_name
m = {
  "manifest_version": "0.3",
  "name": "ttm-telegram",
  "display_name": PARAMS["display"],
  "version": version,
  "description": PARAMS["desc"],
  "long_description": PARAMS["long"],
  "author": {"name": "Toan Tran", "url": "https://github.com/toantranmei"},
  "repository": {"type": "git", "url": "https://github.com/toantranmei/ttm-telegram"},
  "homepage": "https://github.com/toantranmei/ttm-telegram",
  "support": "https://github.com/toantranmei/ttm-telegram/issues",
  "license": "MIT",
  "server": {
    "type": "binary",
    "entry_point": "server/" + bin_name,
    "mcp_config": {"command": cmd, "args": [], "env": PARAMS["env"]},
  },
  "user_config": PARAMS["user_config"],
  "compatibility": {"platforms": [platform]},
}
print(json.dumps(m, ensure_ascii=False, indent=2))
