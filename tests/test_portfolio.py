"""Тесты портфолио: фильтры, пагинация, 404 для черновиков."""

import pytest
from django.urls import reverse

from apps.portfolio.models import Project, Technology


@pytest.mark.django_db
class TestPortfolio:
    def test_detail_404_for_unpublished(self, client, site_settings):
        p = Project.objects.create(
            name="Черновик",
            category=Project.Category.OTHER,
            short_description="x",
            task="x",
            solution="x",
            result="x",
            date="2026-01-01",
            is_published=False,
        )
        response = client.get(p.get_absolute_url())
        assert response.status_code == 404

    def test_filter_by_technology(self, client, site_settings):
        django = Technology.objects.create(name="Django", slug="django")
        vue = Technology.objects.create(name="Vue", slug="vue")

        p1 = Project.objects.create(
            name="Django-проект",
            category=Project.Category.OTHER,
            short_description="x",
            task="x",
            solution="x",
            result="x",
            date="2026-01-01",
            is_published=True,
        )
        p1.technologies.add(django)

        p2 = Project.objects.create(
            name="Vue-проект",
            category=Project.Category.OTHER,
            short_description="x",
            task="x",
            solution="x",
            result="x",
            date="2026-01-01",
            is_published=True,
        )
        p2.technologies.add(vue)

        response = client.get(reverse("portfolio:list"), {"technology": "django"})
        content = response.content.decode()
        assert "Django-проект" in content
        assert "Vue-проект" not in content

    def test_pagination(self, client, site_settings):
        """9 на страницу — 10 проектов, 2 страницы."""
        for i in range(10):
            Project.objects.create(
                name=f"Проект {i}",
                category=Project.Category.OTHER,
                short_description="x",
                task="x",
                solution="x",
                result="x",
                date="2026-01-01",
                is_published=True,
            )
        response = client.get(reverse("portfolio:list"))
        assert len(response.context["page_obj"]) == 9
        assert response.context["page_obj"].paginator.num_pages == 2
