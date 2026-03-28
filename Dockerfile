FROM apache/superset:6.0.0

USER root

# Cài đặt môi trường hệ thống
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium chromium-driver fonts-liberation gettext fontconfig fonts-noto-core && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    fc-cache -fv

# Cài đặt Drivers và Thư viện bổ sung
RUN VENV_SITE_PACKAGES=$(find /app/.venv/lib -maxdepth 2 -name "site-packages") && \
    pip install --no-cache-dir --break-system-packages \
    --target "$VENV_SITE_PACKAGES" \
    psycopg2-binary redis

# Xử lý dịch thuật
RUN mkdir -p /app/superset/translations/vi/LC_MESSAGES
COPY ./translations/vi/messages.po /app/superset/translations/vi/LC_MESSAGES/messages.po

# Script tạo JSON (Đã tối ưu để Frontend Superset đọc được)
COPY <<'EOF' /tmp/translate.py
import json, os
p = "/app/superset/translations/vi/LC_MESSAGES/messages.po"
j = "/app/superset/translations/vi/LC_MESSAGES/messages.json"
if os.path.exists(p):
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()
    translations = {}
    current_id = None
    for line in lines:
        line = line.strip()
        if line.startswith('msgid "'):
            current_id = line[7:-1]
        elif line.startswith('msgstr "') and current_id:
            val = line[8:-1]
            if val:
                translations[current_id] = [val]
                if "%s" in current_id:
                    fe_id = current_id.replace("%s", "{{count}}", 1).replace("%s", "{{value}}")
                    fe_val = val.replace("%s", "{{count}}", 1).replace("%s", "{{value}}")
                    translations[fe_id] = [fe_val]
            current_id = None
    data = {"domain":"superset","locale_data":{"superset":{"":{"domain":"superset","lang":"vi","plural_forms":"nplurals=1; plural=0;"},**translations}}}
    with open(j, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
EOF

# Biên dịch .po sang .mo (cho Backend) và chạy script tạo .json (cho Frontend)
RUN /app/.venv/bin/pybabel compile -d /app/superset/translations -l vi && \
    /app/.venv/bin/python3 /tmp/translate.py && \
    chown -R superset:superset /app/superset/translations

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    CHROMIUM_PATH=/usr/bin/chromium

USER superset
