.PHONY: help up down build logs shell migrate makemigrations createsuperuser \
        test lint format check psql lock

help:
	@echo "make up             - поднять db+web (с пересборкой)"
	@echo "make down           - остановить контейнеры"
	@echo "make logs           - логи web"
	@echo "make shell          - shell внутри web"
	@echo "make migrate        - применить миграции"
	@echo "make makemigrations - создать миграции"
	@echo "make createsuperuser - создать админа"
	@echo "make test           - pytest внутри контейнера"
	@echo "make lint           - ruff + black --check"
	@echo "make format         - black + ruff --fix"
	@echo "make check          - manage.py check"
	@echo "make psql           - psql в контейнере db"
	@echo "make lock           - обновить requirements.lock.txt"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f web

shell:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web pytest

lint:
	docker compose exec web ruff check .
	docker compose exec web black --check .

format:
	docker compose exec web black .
	docker compose exec web ruff check --fix .

check:
	docker compose exec web python manage.py check

psql:
	docker compose exec db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

lock:
	docker compose exec web pip freeze > requirements.lock.txt