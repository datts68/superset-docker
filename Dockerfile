FROM apache/superset:6.0.0

USER root

# 1. Cài đặt Chromium, Drivers và Fonts Tiếng Việt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libgbm1 \
    libasound2 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxtst6 \
    libpango-1.0-0 \
    libcairo2 \
    fonts-noto-core \
    fontconfig \
    gettext && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN fc-cache -fv

# 2. Cài đặt driver DB vào venv
RUN VENV_SITE_PACKAGES=$(find /app/.venv/lib -maxdepth 2 -name "site-packages") && \
    pip install --no-cache-dir --break-system-packages \
    --target "$VENV_SITE_PACKAGES" \
    psycopg2-binary redis

# 3. Import file dịch và biên dịch
RUN mkdir -p /app/superset/translations/vi/LC_MESSAGES
COPY --chown=superset:superset messages.po /app/superset/translations/vi/LC_MESSAGES/messages.po

# Cấp quyền và biên dịch sang .mo (Backend)
RUN chown -R superset:superset /app/superset/translations && \
    /app/.venv/bin/pybabel compile -d /app/superset/translations -l vi && \
    /app/.venv/bin/python3 /app/superset/translations/utils.py

# 4. Thiết lập môi trường Chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    CHROMIUM_PATH=/usr/bin/chromium

USER superset
