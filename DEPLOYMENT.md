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

## Kết quả kiểm tra URL công khai

Kiểm tra bằng PowerShell `curl.exe` ngày 29/09/2026 tại URL công khai ở trên.

```powershell
$URL = 'https://day12-agent-un6x.onrender.com'
curl.exe -i "$URL/health"
curl.exe -i "$URL/ready"
curl.exe -i -X POST "$URL/ask" -H "Content-Type: application/json" --data-raw '{"question":"Hello"}'
```

```text
GET /health → HTTP 200
{"status":"ok","service":"day12-agent","version":"1.0.0"}

GET /ready → HTTP 200
{"status":"ready","redis":true}

POST /ask, không có X-API-Key → HTTP 401
{"detail":"invalid or missing API key"}
```

## Bằng chứng ảnh

- `screenshots/dashboard.png` — trang Render hiển thị web service và Key Value.
- `screenshots/health.png` — kết quả gọi `/health` trên URL công khai.

Ảnh sẽ được thêm sau khi chụp dashboard và kết quả health, không hiển thị giá trị secret.
