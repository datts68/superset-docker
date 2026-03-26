import os

# --- Security ---
SECRET_KEY = "XT306XYZTHANHNAM"

# --- Database & Redis ---
SQLALCHEMY_DATABASE_URI = "postgresql://superset:Xt306xyZ@superset_db:5432/superset"
SQLALCHEMY_EXAMPLES_URI = "postgresql://superset:Xt306xyZ@superset_db:5432/superset"
REDIS_URL = "redis://:Xt306xyZ@superset_redis:6379/0"


# --- Celery Configuration ---
class CeleryConfig:
    broker_url = REDIS_URL
    imports = ("superset.sql_lab", "superset.tasks", "superset.tasks.thumbnails")
    result_backend = REDIS_URL
    worker_prefetch_multiplier = 1
    task_acks_late = True


CELERY_CONFIG = CeleryConfig

# --- Screenshot & Download Dashboard ---
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_EXECUTABLE_PATH = "/usr/bin/chromium"
WEBDRIVER_BASEURL = "http://superset:8088/"

WEBDRIVER_OPTION_ARGS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--window-size=1200,1200",
]

# --- Feature Flags ---
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "ALERTS_REPORTS": True,
    "ALLOW_DASHBOARD_EXPORT": True,
    "DASHBOARD_RBAC": True,
}

# --- Cấu hình BỎ QUA CSRF cho API (QUAN TRỌNG) ---
WTF_CSRF_ENABLED = True
# Tắt kiểm tra CSRF đối với các Header Authorization (JWT)
WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_EXEMPT_LIST = [
    "superset.views.api.security.guest_token",
    "/api/v1/security/guest_token/",
    "/api/v1/security/guest_token",
    "/api/v1/security/login",
    "/api/v1/security/refresh",
]

# --- Embedding & CORS ---
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "origins": ["*"],
    "expose_headers": ["*"],
}

# Cho phép nhúng Iframe
HTTP_HEADERS = {"X-Frame-Options": "ALLOWALL"}
TALISMAN_CONFIG = {
    "content_security_policy": {"frame-ancestors": ["*"]},
    "force_https": False,
    "session_cookie_secure": False,
    "session_cookie_samesite": None,
}

# Cookie settings cho môi trường không có HTTPS (Local/IP)
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

# Cho phép Guest User xem các tài nguyên được chỉ định trong Guest Token
GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_EXPIRY_SECONDS = 3600

# --- Localization ---
BABEL_DEFAULT_LOCALE = "vi"
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "vi": {"flag": "vn", "name": "Vietnamese"},
}

ENABLE_PROXY_FIX = True
