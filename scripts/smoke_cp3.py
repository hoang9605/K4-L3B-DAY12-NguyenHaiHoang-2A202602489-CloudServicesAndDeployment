"""Gửi một request có xác thực tới agent đang chạy trên máy."""

from pathlib import Path
import sys
from uuid import uuid4

import httpx
from dotenv import dotenv_values


repo_root = Path(__file__).resolve().parents[1]
api_key = dotenv_values(repo_root / ".env").get("AGENT_API_KEY")
if not api_key:
    raise SystemExit("Thiếu AGENT_API_KEY trong .env")

# Mỗi lần thử dùng user riêng để không vướng giới hạn 10 request/phút.
user_id = f"smoke-{uuid4().hex[:8]}"
response = httpx.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "Docker là gì?"},
    headers={"X-API-Key": api_key, "X-User-Id": user_id},
    timeout=10,
    trust_env=False,
)
# PowerShell có thể dùng cp1252; chuyển stdout sang UTF-8 trước khi in tiếng Việt.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
print(f"HTTP {response.status_code}")
print(response.text)
raise SystemExit(0 if response.status_code == 200 else 1)
