import os

# --- Security ---
SECRET_KEY = "XT306XYZTHANHNAM"

# --- Database & Redis ---
SQLALCHEMY_DATABASE_URI = "postgresql://superset:Xt306xyZ@superset_db:5432/superset"
SQLALCHEMY_EXAMPLES_URI = "postgresql://superset:Xt306xyZ@superset_db:5432/superset"
REDIS_URL = "redis://:Xt306xyZ@superset_redis:6379/0"


# --- Celery ---
class CeleryConfig:
    broker_url = REDIS_URL
    imports = ("superset.sql_lab", "superset.tasks", "superset.tasks.thumbnails")
    result_backend = REDIS_URL
    worker_prefetch_multiplier = 1
    task_acks_late = True


CELERY_CONFIG = CeleryConfig

# --- Screenshots (Chromium) ---
WEBDRIVER_TYPE = "chromium"
WEBDRIVER_EXECUTABLE_PATH = "/usr/bin/chromium"
WEBDRIVER_BASEURL = "http://superset:8088/"
WEBDRIVER_OPTION_ARGS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--window-size=1920,1080",
]

# --- Feature Flags ---
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "ALERTS_REPORTS": True,
    "ALLOW_DASHBOARD_EXPORT": True,
    "DASHBOARD_RBAC": True,
    "GENERIC_CHART_AXES": True,  # Hỗ trợ tốt hơn cho các loại biểu đồ ở bản 5.x
}

# --- CORS & Embedding ---
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "origins": ["*"],
}

# HTTP Headers & CSP (Để CSS nhận)
HTTP_HEADERS = {"X-Frame-Options": "ALLOWALL"}
TALISMAN_CONFIG = {
    "content_security_policy": {
        "frame-ancestors": ["*"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        "img-src": ["'self'", "data:", "blob:", "*"],
    },
    "force_https": False,
    "session_cookie_secure": False,
    "session_cookie_samesite": None,
}

# Cookie settings
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

# Guest Access
GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_EXPIRY_SECONDS = 3600

# --- Localization (Vietnamese) ---
BABEL_DEFAULT_LOCALE = "vi"
LANGUAGES = {
    "vi": {"flag": "vn", "name": "Vietnamese"},
    "en": {"flag": "us", "name": "English"},
}


def get_locale():
    return "vi"


BABEL_LOCALE_SELECTOR_FUNC = get_locale
BABEL_DEFAULT_TIMEZONE = "Asia/Ho_Chi_Minh"

ENABLE_PROXY_FIX = True
