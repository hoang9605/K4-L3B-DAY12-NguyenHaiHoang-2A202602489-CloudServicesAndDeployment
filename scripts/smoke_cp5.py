"""Kiểm tra 5 endpoint/guard trên Render mà không in DEPLOY_API_KEY."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import dotenv_values


repo_root = Path(__file__).resolve().parents[1]
api_key = dotenv_values(repo_root / ".env").get("DEPLOY_API_KEY")
if not api_key:
    raise SystemExit("Thiếu DEPLOY_API_KEY trong .env")

base_url = "https://day12-agent-un6x.onrender.com"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with httpx.Client(timeout=60, trust_env=False) as client:
    checks = []
    for path in ("/health", "/ready"):
        response = client.get(base_url + path)
        print(f"GET {path}: HTTP {response.status_code} {response.text}")
        checks.append(response.status_code == 200)

    response = client.post(base_url + "/ask", json={"question": "Hello"})
    print(f"POST /ask (không key): HTTP {response.status_code} {response.text}")
    checks.append(response.status_code == 401)

    # Chỉ gửi key trong header; không bao giờ in nó ra stdout hay tài liệu.
    headers = {"X-API-Key": api_key, "X-User-Id": "sv-test"}
    response = client.post(base_url + "/ask", json={"question": "Deploy là gì?"}, headers=headers)
    print(f"POST /ask (có key): HTTP {response.status_code} {response.text}")
    checks.append(response.status_code == 200)

    # User riêng mỗi lần chạy để phép đo 10/phút không vướng lượt thử trước.
    rate_user = "sv-rate-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    rate_headers = {"X-API-Key": api_key, "X-User-Id": rate_user}
    statuses = [
        client.post(base_url + "/ask", json={"question": "test"}, headers=rate_headers).status_code
        for _ in range(15)
    ]
    print("Rate limit, 15 request cùng user: " + " ".join(map(str, statuses)))
    checks.append(statuses == [200] * 10 + [429] * 5)

if not all(checks):
    raise SystemExit("Có phép kiểm tra CP5 chưa đúng kết quả mong đợi")
