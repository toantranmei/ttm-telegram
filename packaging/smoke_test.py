"""Kiểm tra nhanh binary MCP: initialize + tools/list qua stdio. Dùng: smoke_test.py <binary> <số tool tối thiểu>."""
import json, os, subprocess, sys, select

binary, minimum = sys.argv[1], int(sys.argv[2])
env = dict(os.environ, JIRA_URL="https://example.invalid", JIRA_PERSONAL_TOKEN="x",
           TELEGRAM_API_ID="1", TELEGRAM_API_HASH="x" * 32)
p = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

def send(o):
    p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()

def read(timeout=30):
    r, _, _ = select.select([p.stdout], [], [], timeout)
    return p.stdout.readline() if r else ""

send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "0"}}})
if '"result"' not in read():
    print("FAIL: initialize"); p.kill(); sys.exit(1)
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
line = read()
p.kill()
if not line:
    print("FAIL: tools/list timeout"); sys.exit(1)
n = len(json.loads(line)["result"]["tools"])
print(f"OK: {n} tools")
sys.exit(0 if n >= minimum else 1)
