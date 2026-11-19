# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

# Не создавать .pyc, не буферизовать stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Системные зависимости:
# - libpq5 не нужен (psycopg[binary] тащит свой libpq)
# - Pillow 11 идёт wheel'ом, тоже без системных пакетов
# Оставляем slim-образ без лишнего.
WORKDIR /app

# Non-root пользователь
RUN addgroup --system app && adduser --system --ingroup app app

# Сначала только зависимости — кэш слоя
COPY requirements.txt requirements.lock.txt ./
RUN pip install -r requirements.lock.txt

# Потом код
COPY . .
RUN chown -R app:app /app
USER app

# collectstatic/migrate — в entrypoint, чтобы выполнялись при каждом старте
ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 8000