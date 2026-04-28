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

# --- Theme & UI (Version 6.0.0) ---
DEFAULT_THEME_CONTROLS = {
    "default_scheme": "light",  # Ép mặc định là bản sáng
    "prefers_color_scheme": False,  # Không tự nhảy theo trình duyệt
}

# --- Feature Flags ---
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "ALERTS_REPORTS": True,
    "ALLOW_DASHBOARD_EXPORT": True,
    "DASHBOARD_RBAC": True,
    # "ENABLE_SUPERSET_META_DB": True, # Nếu muốn kích hoạt Superset Meta Database (kết nối nhiều database)
    # "DARK_MODE_PREFERENCE": False, # Ẩn nút chuyển Dark Mode ở menu người dùng
    "THUMBNAILS": True,
    "DASHBOARD_CACHE_SCREENSHOT": True,
    "ENABLE_DASHBOARD_SCREENSHOT_ENDPOINTS": True,
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
    "content_security_policy": {
        "frame-ancestors": ["*"],
        # 'unsafe-inline' cho phép các tùy chỉnh CSS trong Dashboard hoạt động:
        "style-src": ["'self'", "'unsafe-inline'"],
        # 'unsafe-eval' thường cần thiết cho một số biểu đồ phức tạp ở bản mới:
        "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        # Cho phép load icon SVG từ CSS:
        "img-src": ["'self'", "data:", "blob:", "*"],
    },
    "force_https": False,
    "session_cookie_secure": False,
    "session_cookie_samesite": None,
}

# Cookie settings cho môi trường không có HTTPS (Local/IP)
# Khi chạy với HTTPS => đổi Lax thành None và Secure thành True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

# Cho phép Guest User xem các tài nguyên được chỉ định trong Guest Token
GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_JWT_EXPIRY_SECONDS = 3600

# --- Localization ---
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


# --- CSS FIX (Ẩn các chuỗi không dịch được) ---
# Tự động chèn CSS này vào mọi Dashboard
# CUSTOM_STACKTRACE = False
# DEFAULT_SECTION_NAME = "General"

# # Cách ẩn thông qua CSS chèn vào Header
# CSS_OVERRIDE = """
# """
