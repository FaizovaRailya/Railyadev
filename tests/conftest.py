"""Общие фикстуры pytest."""

import pytest

from apps.core.models import SiteSettings
from apps.portfolio.models import Project, Technology
from apps.reviews.models import Testimonial
from apps.services.models import Service


@pytest.fixture
def site_settings(db):
    """SiteSettings для шаблонов (навбар, футер)."""
    return SiteSettings.objects.create(
        name="Тестовый бренд",
        slogan="Тестовый слоган",
        email="test@example.com",
        phone="+7 999 000-00-00",
        city="Москва",
        telegram="https://t.me/test",
        max_url="https://max.ru/test",
    )


@pytest.fixture
def technology(db):
    return Technology.objects.create(name="Django", slug="django")


@pytest.fixture
def project(db, technology):
    p = Project.objects.create(
        name="Тестовый кейс",
        category=Project.Category.CORPORATE,
        short_description="Краткое описание",
        task="Задача",
        solution="Решение",
        result="Результат",
        date="2026-01-01",
        is_published=True,
        is_featured=True,
    )
    p.technologies.add(technology)
    return p


@pytest.fixture
def service(db):
    return Service.objects.create(
        name="Разработка сайта",
        short_description="Краткое",
        full_description="Полное",
        price_from="50000.00",
        duration="2 недели",
        is_active=True,
    )


@pytest.fixture
def testimonial(db):
    return Testimonial.objects.create(
        name="Иван",
        company="ООО Ромашка",
        text="Отличная работа",
        rating=5,
        date="2026-01-01",
        is_published=True,
    )
