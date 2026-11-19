"""
Настройки для продакшена.

HTTPS-редиректы, secure cookies, HSTS, SMTP email.
Защита от случайного DEBUG=True.
"""

from .base import *  # noqa: F401, F403

DEBUG = False

# Защита от случайного деплоя с DEBUG=True:
# если кто-то поправит base.py и вернёт DEBUG=True,
# прод не запустится — лучше упасть на старте.
if DEBUG:
    raise RuntimeError("DEBUG must be False in prod. Проверьте config/settings/prod.py и .env.")

# ============================================================
# Безопасность (только в проде)
# ============================================================
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ============================================================
# Email (SMTP)
# ============================================================
# EMAIL_BACKEND, EMAIL_HOST и т.д. читаются из .env — в проде
# там должен быть django.core.mail.backends.smtp.EmailBackend.
