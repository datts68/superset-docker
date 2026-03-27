FROM apache/superset:6.0.0

USER root

# 1. Cài đặt Chromium, Drivers và Fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium chromium-driver fonts-liberation gettext fontconfig fonts-noto-core && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN fc-cache -fv

# 2. Cài đặt driver DB vào venv
RUN VENV_SITE_PACKAGES=$(find /app/.venv/lib -maxdepth 2 -name "site-packages") && \
    pip install --no-cache-dir --break-system-packages \
    --target "$VENV_SITE_PACKAGES" \
    psycopg2-binary redis


# 3. Import file dịch và biên dịch (Ép tạo JSON cho Dashboard)
RUN mkdir -p /app/superset/translations/vi/LC_MESSAGES
COPY ./translations/vi/messages.po /app/superset/translations/vi/LC_MESSAGES/messages.po

# Sử dụng Heredoc với dấu nháy đơn quanh EOF để ngăn Docker can thiệp vào nội dung
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
            if val: # Chỉ lấy nếu đã được dịch
                translations[current_id] = [val]
            current_id = None

    data = {
        "domain": "superset",
        "locale_data": {
            "superset": {
                "": {
                    "domain": "superset", 
                    "lang": "vi", 
                    "plural_forms": "nplurals=1; plural=0;"
                },
                **translations
            }
        }
    }
    
    with open(j, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Success! Generated {len(translations)} keys.")
EOF

# Thực thi biên dịch và đồng bộ
RUN /app/.venv/bin/pybabel compile -d /app/superset/translations -l vi && \
    /app/.venv/bin/python3 /tmp/translate.py && \
    mkdir -p /app/superset/static/assets/ && \
    cp /app/superset/translations/vi/LC_MESSAGES/messages.json /app/superset/static/assets/messages.json

RUN chown -R superset:superset /app/superset/translations /app/superset/static/assets/


# 4. Thiết lập môi trường
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    CHROMIUM_PATH=/usr/bin/chromium

USER superset
