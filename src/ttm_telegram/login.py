"""Đăng nhập Telegram một lần để tạo file session trên máy bạn, rồi liệt kê nhóm để lấy group_id."""

import asyncio

from telethon import TelegramClient

from .config import API_HASH, API_ID, SESSION, ensure_session_dir


async def _main() -> None:
    ensure_session_dir()
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        me = await client.get_me()
        print(f"Đăng nhập thành công: {me.first_name}")
        print("\nDANH SÁCH NHÓM (dùng group_id cho ALLOWED_GROUP_IDS)\n")
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                print(f"Group ID: {dialog.id} | Name: {dialog.name}")


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
