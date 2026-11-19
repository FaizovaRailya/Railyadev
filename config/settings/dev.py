"""
Настройки для локальной разработки.

DEBUG=True, письма в консоль, ALLOWED_HOSTS=*.
Никаких HTTPS-редиректов, чтобы сайт открывался по http://localhost:8000.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Письма в консоль — удобно видеть, что было отправлено
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Без HTTPS-редиректов в dev
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
