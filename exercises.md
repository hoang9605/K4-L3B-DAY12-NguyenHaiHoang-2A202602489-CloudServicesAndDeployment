# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: điền nội dung phản ánh dưới mỗi câu hỏi.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Nguyễn Hải Hoàng  Mã học viên: 2A202602489

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Nếu quên đặt `AGENT_API_KEY` khi tạo service Render, app dừng ngay lúc khởi động và log báo thiếu cấu hình. Nhờ vậy tôi biết phải sửa Environment trước khi công bố URL; nếu dùng khóa mặc định `changeme`, app vẫn chạy và người khác có thể đoán khóa để gọi `/ask`.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Tôi gọi `/ask` trên container local và thu được một dòng: `{"event": "ask_completed", "level": "info", "timestamp": "2026-09-29T04:49:13.467965+00:00", "user_id": "smoke-0cc2afd7", "tokens_in": 3, "tokens_out": 37, "cost_usd": 2.265e-05}`. Tôi có thể lọc các dòng có `event=ask_completed` để đếm số lượt hỏi, và cộng `cost_usd` theo `user_id` để theo dõi chi phí. Một dòng `print("đã trả lời xong")` không có các trường để làm hai việc đó.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 1.73 GB (1730 MB theo `docker images`) |
| Multi-stage | 271 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Tôi build lại Dockerfile một stage gốc với tag `agent:single` và bản hiện tại với tag `agent:multi`; Docker báo 1.73 GB và 271 MB, chênh khoảng 1.46 GB. Phần lớn chênh lệch đến từ base `python:3.11` đầy đủ so với `python:3.11-slim`; bản đầu còn giữ các lớp cài đặt trong image cuối, còn bản multi-stage chỉ mang thư viện đã cài sang runtime và dùng `pip --no-cache-dir`. Vì đã thay cả base image lẫn cách build, không thể quy toàn bộ mức giảm cho riêng multi-stage.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Tôi đổi một ký tự ở comment trong `app/main.py` rồi build lại: `COPY requirements.txt`, `RUN pip install` và `COPY --from=builder` đều hiện `CACHED`; `COPY app`, `COPY utils` và `RUN useradd` chạy lại vì nằm sau lớp `COPY app`. Nếu `COPY . .` đứng trước `RUN pip install`, mỗi lần sửa source sẽ làm lớp `COPY` đổi và pip phải chạy lại dù `requirements.txt` không đổi.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Giả sử code Python có lỗ hổng thực thi lệnh: kẻ tấn công trước hết chạy lệnh trong container. Nếu process là root và container có thêm cấu hình nguy hiểm như mount Docker socket hoặc quyền đặc biệt, họ có thể dùng quyền đó để tác động lên host. `USER appuser` khiến lệnh bị chiếm chỉ có quyền user thường trong container, giảm khả năng đi tiếp trong chuỗi này; riêng việc chạy root trong container không tự động biến thành root trên host.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Tối đa 20 request: gửi 10 lần ở giây 59 của phút trước, rồi 10 lần ở giây 00 của phút sau. Bộ đếm theo phút vừa reset nên vẫn cho qua, dù cả 20 request dồn vào khoảng hai giây. Cửa sổ trượt nhìn lại 60 giây gần nhất nên chặn đợt thứ hai.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit giới hạn số request trong 60 giây và trả 429; cost guard giới hạn tổng chi phí theo user trong tháng UTC và trả 402. Nếu một user đã tiêu quá 10 USD nhưng một phút qua chưa gọi lần nào, rate limit cho qua còn cost guard chặn. Ngược lại, nếu user đã gọi đủ 10 lần trong 60 giây nhưng chi phí mới rất nhỏ, cost guard còn cho qua còn rate limit chặn lượt kế tiếp.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Redis mất kết nối trước; cả ba container cùng bị endpoint gộp báo không khỏe dù process vẫn sống. Orchestrator sau đó đánh dấu cả ba unhealthy và có thể restart chúng lặp lại trong 30 giây Redis lỗi, làm các request đang xử lý bị gián đoạn mà không sửa được Redis. Khi Redis trở lại, container còn phải khởi động và qua health check lại. Tách `/health` chỉ kiểm tra process và `/ready` kiểm tra Redis giúp load balancer tạm ngừng gửi request mà không restart cả cụm vô ích.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Tôi gửi ba lượt `/ask` cùng `X-User-Id` lần lượt vào agent 1, 2, 3; `history_length` trả 0, 2, 4 vì mỗi lượt thêm một message user và một message assistant vào Redis chung. Nếu dùng dict Python riêng cho từng container, mỗi container chỉ thấy lịch sử của nó: ba lượt đầu sẽ là 0, 0, 0; các lượt sau có thể tăng hoặc giảm theo container nhận request.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Tôi không gặp lỗi trong quá trình Render build/deploy. Lỗi thực tế xuất hiện khi kiểm tra URL cloud từ máy local: có lần `pytest tests/test_cp5.py` báo `ConnectTimeout` hoặc `getaddrinfo failed` ở `/health`, `/ready` hoặc `/ask`. Tôi đối chiếu với `curl.exe` và chạy lại test: endpoint vẫn trả 200/401, cuối cùng CP5 đạt 9 passed, 4 skipped. Tôi kết luận đây là sự cố kết nối/DNS chập chờn trên đường kiểm tra, nên không sửa code hay `REDIS_URL` khi chưa có bằng chứng service lỗi.
