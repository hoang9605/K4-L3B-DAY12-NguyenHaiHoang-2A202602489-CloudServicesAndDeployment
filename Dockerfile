FROM python:3.11-slim AS builder

WORKDIR /app
# Tách dependency khỏi source để sửa code không phải chạy lại pip install.
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Runtime chỉ nhận thư viện đã cài, không mang theo công cụ build.
COPY --from=builder /install /usr/local
COPY app ./app
COPY utils ./utils

# Chạy ứng dụng bằng user thường để giảm quyền trong container.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000
# Liveness dùng /health; đọc PORT để khớp cổng do cloud cấp.
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8000') + '/health', timeout=3).read()" || exit 1

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
