# Thông tin triển khai — CP5

## Học viên và repository

| Mục | Nội dung |
|---|---|
| Họ và tên | Nguyễn Hải Hoàng |
| Mã học viên | 2A202602489 |
| Repository | https://github.com/hoang9605/K4-L3B-DAY12-NguyenHaiHoang-2A202602489-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|---|---|
| Platform | Render Blueprint |
| Public URL | https://day12-agent-un6x.onrender.com |
| Ngày kiểm tra | 29/09/2026 |

## Biến môi trường trên Render

Chỉ ghi tên và nguồn cấu hình, không ghi giá trị secret.

| Biến | Nguồn |
|---|---|
| `PORT` | Render tự cấp; Dockerfile đọc `${PORT:-8000}` |
| `AGENT_API_KEY` | Secret nhập khi tạo Blueprint |
| `REDIS_URL` | Internal connection string của `day12-redis` qua Blueprint |
| `RATE_LIMIT_PER_MINUTE` | Blueprint: 10 |
| `MONTHLY_BUDGET_USD` | Blueprint: 10.0 |
| `LOG_LEVEL` | Blueprint: INFO |

## Lệnh kiểm tra URL công khai

Chạy trong PowerShell từ gốc repository. Script đọc `DEPLOY_API_KEY` từ `.env` cục bộ để kiểm tra có xác thực và rate limit, nhưng không in khóa. Dấu `\` xuống dòng của Bash không dùng được trong PowerShell.

```powershell
$URL = 'https://day12-agent-un6x.onrender.com'
curl.exe -i "$URL/health"
curl.exe -i "$URL/ready"
curl.exe -i -X POST "$URL/ask" -H "Content-Type: application/json" --data-raw '{"question":"Hello"}'
.\.venv\Scripts\python.exe scripts\smoke_cp5.py
```

## Kết quả chạy thật

Output ngày 29/09/2026 (câu trả lời và user ID không chứa secret):

```text
GET /health → HTTP 200
{"status":"ok","service":"day12-agent","version":"1.0.0"}

GET /ready → HTTP 200
{"status":"ready","redis":true}

POST /ask, không có X-API-Key → HTTP 401
{"detail":"invalid or missing API key"}

POST /ask, có X-API-Key hợp lệ → HTTP 200
{"answer":"Câu hỏi hay. Deploy là gì thường được giải quyết bằng cách chuẩn hóa môi trường chạy: cùng một image chạy giống nhau ở laptop và trên cloud.","user_id":"sv-test","history_length":0,"cost_usd":2.145e-05,"tokens":{"in":3,"out":35}}

Rate limit, 15 request cùng user:
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

`pytest tests/test_cp5.py -v --tb=short`: 9 passed, 4 skipped (các test local fallback).

## Bằng chứng ảnh

- `screenshots/dashboard.png` — Blueprint hiển thị `day12-agent` ở trạng thái Deployed và `day12-redis` ở trạng thái Available.
- `screenshots/health.png` — kết quả `/health` HTTP 200 và `/ready` HTTP 200 trên URL công khai.

Hai ảnh đã được lưu trong repository và không hiển thị giá trị secret.
