"""Kiểm tra nhanh binary MCP: initialize + tools/list qua stdio (chạy được trên Windows, macOS, Linux).

Dùng: smoke_test.py <đường dẫn binary> <số tool tối thiểu>
"""
import json
import os
import queue
import subprocess
import sys
import threading

binary, minimum = sys.argv[1], int(sys.argv[2])
env = dict(os.environ, JIRA_URL="https://example.invalid", JIRA_PERSONAL_TOKEN="x",
           TELEGRAM_API_ID="1", TELEGRAM_API_HASH="x" * 32)
p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, text=True, env=env)
lines: "queue.Queue[str]" = queue.Queue()
threading.Thread(target=lambda: [lines.put(l) for l in p.stdout], daemon=True).start()


def send(o):
    p.stdin.write(json.dumps(o) + "\n")
    p.stdin.flush()


def read(timeout=60):
    try:
        return lines.get(timeout=timeout)
    except queue.Empty:
        return ""


try:
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "0"}}})
    if '"result"' not in read():
        print("FAIL: initialize")
        sys.exit(1)
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    line = read()
    if not line:
        print("FAIL: tools/list timeout")
        sys.exit(1)
    n = len(json.loads(line)["result"]["tools"])
    print(f"OK: {n} tools")
    sys.exit(0 if n >= minimum else 1)
finally:
    p.kill()
