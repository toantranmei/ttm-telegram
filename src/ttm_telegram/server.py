"""ttm-telegram: MCP server (stdio) đọc tin nhắn nhóm Telegram bằng tài khoản của bạn.

Chạy trên máy bạn. Dữ liệu chỉ đi giữa máy bạn và Telegram, không gửi qua dịch vụ nào của bên thứ ba.
"""

from datetime import datetime, timedelta, timezone

from fastmcp import FastMCP
from telethon import TelegramClient

from .config import (
    ALLOW_ALL_GROUPS,
    ALLOWED_GROUPS,
    API_HASH,
    API_ID,
    SESSION,
    TZ,
    ensure_session_dir,
)

mcp = FastMCP("ttm-telegram")


def _client() -> TelegramClient:
    ensure_session_dir()
    return TelegramClient(SESSION, API_ID, API_HASH)


async def _resolve_group(client, group_id: int):
    if not ALLOW_ALL_GROUPS and group_id not in ALLOWED_GROUPS:
        raise ValueError(
            "Nhóm này chưa được cấp quyền. Thêm group_id vào ALLOWED_GROUP_IDS (hoặc đặt ALL)."
        )
    async for dialog in client.iter_dialogs():
        if dialog.id == group_id and dialog.is_group:
            return dialog.entity
    raise ValueError("Không tìm thấy nhóm Telegram với group_id này.")


@mcp.tool()
async def list_groups() -> list[dict]:
    """Danh sách nhóm Telegram được phép đọc (theo ALLOWED_GROUP_IDS)."""
    result = []
    async with _client() as client:
        async for dialog in client.iter_dialogs():
            if dialog.is_group and (ALLOW_ALL_GROUPS or dialog.id in ALLOWED_GROUPS):
                result.append({"group_id": dialog.id, "name": dialog.name})
    return result


@mcp.tool()
async def get_messages(group_id: int, start_date: str, end_date: str, limit: int = 500) -> dict:
    """Đọc tin nhắn chữ của một nhóm trong khoảng ngày.

    start_date, end_date: YYYY-MM-DD, tính theo múi giờ TELEGRAM_TZ (mặc định Asia/Ho_Chi_Minh).
    limit: tối đa 1000.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=TZ)
    end = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=TZ) + timedelta(days=1)
    if end <= start:
        raise ValueError("Khoảng ngày không hợp lệ.")

    limit = max(1, min(limit, 1000))
    results: list[dict] = []
    truncated = False

    async with _client() as client:
        entity = await _resolve_group(client, group_id)
        async for msg in client.iter_messages(entity, offset_date=end.astimezone(timezone.utc)):
            if msg.date < start.astimezone(timezone.utc):
                break
            if not msg.message:
                continue
            if len(results) >= limit:
                truncated = True
                break
            results.append({
                "message_id": msg.id,
                "sender_id": msg.sender_id,
                "date": msg.date.astimezone(TZ).isoformat(),
                "text": msg.message,
                "reply_to_id": msg.reply_to.reply_to_msg_id if msg.reply_to else None,
            })

    return {
        "group_id": group_id,
        "start_date": start_date,
        "end_date": end_date,
        "count": len(results),
        "truncated": truncated,
        "messages": results,
    }


@mcp.tool()
async def search_messages(group_id: int, keyword: str, limit: int = 100) -> list[dict]:
    """Tìm tin nhắn trong nhóm theo từ khóa. limit tối đa 200."""
    limit = max(1, min(limit, 200))
    results: list[dict] = []
    async with _client() as client:
        entity = await _resolve_group(client, group_id)
        async for msg in client.iter_messages(entity, search=keyword, limit=limit):
            results.append({
                "message_id": msg.id,
                "sender_id": msg.sender_id,
                "date": msg.date.astimezone(TZ).isoformat(),
                "text": msg.message,
            })
    return results


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
