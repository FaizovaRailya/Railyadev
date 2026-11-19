"""Тесты views."""

import pytest
from django.core.cache import cache
from django.urls import reverse

from apps.core.models import ContactRequest


@pytest.mark.django_db
class TestPublicPages:
    def test_home_200(self, client, site_settings):
        response = client.get(reverse("core:home"))
        assert response.status_code == 200

    def test_about_200(self, client, site_settings):
        assert client.get(reverse("core:about")).status_code == 200

    def test_contact_200(self, client, site_settings):
        assert client.get(reverse("core:contact")).status_code == 200

    def test_privacy_200(self, client, site_settings):
        assert client.get(reverse("core:privacy")).status_code == 200

    def test_portfolio_list_200(self, client, site_settings):
        assert client.get(reverse("portfolio:list")).status_code == 200

    def test_services_list_200(self, client, site_settings):
        assert client.get(reverse("services:list")).status_code == 200

    def test_blog_list_200(self, client, site_settings):
        assert client.get(reverse("blog:list")).status_code == 200


@pytest.mark.django_db
class TestContactView:
    def setup_method(self):
        cache.clear()

    def test_post_creates_request_and_redirects(self, client, site_settings):
        response = client.post(
            reverse("core:contact"),
            {
                "name": "Иван",
                "email": "ivan@example.com",
                "phone": "",
                "message": "Нужен сайт на Django, подробности в письме.",
                "website": "",
            },
        )
        assert response.status_code == 302
        assert response.url == reverse("core:contact")
        assert ContactRequest.objects.count() == 1
        req = ContactRequest.objects.first()
        assert req.name == "Иван"
        assert req.ip_address is not None

    def test_honeypot_blocks_submission(self, client, site_settings):
        response = client.post(
            reverse("core:contact"),
            {
                "name": "Бот",
                "email": "bot@example.com",
                "message": "Достаточно длинное сообщение для бота",
                "website": "http://spam.com",
            },
        )
        assert response.status_code == 200  # рендерится форма с ошибкой
        assert ContactRequest.objects.count() == 0

    def test_rate_limit(self, client, site_settings):
        """Не более 3 заявок в час с одного IP."""
        data = {
            "name": "Иван",
            "email": "ivan@example.com",
            "message": "Достаточно длинное сообщение",
            "website": "",
        }
        for _ in range(3):
            client.post(reverse("core:contact"), data)

        # 4-я заявка — должна быть заблокирована rate limit
        response = client.post(reverse("core:contact"), data, follow=True)
        assert ContactRequest.objects.count() == 3
        assert "Слишком много заявок" in response.content.decode()
