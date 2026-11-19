"""
Настройки для pytest: PostgreSQL (без SQLite).

Параметры БД берутся из env с fallback на локальный Docker (localhost:5434).
В CI задаются через env: localhost:5432.
"""

import os

from .dev import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "portfolio"),
        "USER": os.environ.get("POSTGRES_USER", "portfolio"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "portfolio"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5434"),
    }
}

# Письма не отправляются в тестах
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Ускоряет хеширование паролей в тестах
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]