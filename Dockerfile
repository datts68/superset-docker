FROM apache/superset:6.0.0

USER root

# Cài đặt Chromium và driver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libgbm1 \
    libasound2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Tìm đúng thư viện của venv để cài psycopg2 và redis vào đó
RUN VENV_SITE_PACKAGES=$(find /app/.venv/lib -maxdepth 2 -name "site-packages") && \
    pip install --no-cache-dir --break-system-packages \
    --target "$VENV_SITE_PACKAGES" \
    psycopg2-binary redis

# Thiết lập đường dẫn Chromium cho Superset
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    CHROMIUM_PATH=/usr/bin/chromium

USER superset
