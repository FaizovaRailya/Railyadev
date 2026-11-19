"""Тесты админки."""

import pytest
from django.contrib.auth import get_user_model

from apps.core.models import ContactRequest, SiteSettings

User = get_user_model()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin", email="admin@example.com", password="pass12345"
    )


@pytest.mark.django_db
class TestAdminAccess:
    def test_guest_cannot_access_admin(self, client):
        response = client.get("/admin/")
        assert response.status_code == 302  # редирект на login
        assert "/admin/login/" in response.url

    def test_admin_can_login(self, client, admin_user):
        client.force_login(admin_user)
        response = client.get("/admin/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestSiteSettingsAdmin:
    def test_add_forbidden_if_exists(self, client, admin_user):
        """Кнопки «Добавить» нет, если запись уже создана."""
        SiteSettings.load()  # создаст запись
        client.force_login(admin_user)
        response = client.get("/admin/core/sitesettings/add/")
        # has_add_permission=False → 403
        assert response.status_code == 403


@pytest.mark.django_db
class TestContactRequestAdmin:
    def test_export_csv_action(self, client, admin_user):
        ContactRequest.objects.create(
            name="Иван",
            email="i@example.com",
            message="Текст заявки",
        )
        client.force_login(admin_user)
        response = client.post(
            "/admin/core/contactrequest/",
            {
                "action": "export_csv",
                "_selected_action": ContactRequest.objects.values_list("pk", flat=True),
            },
        )
        assert response.status_code == 200
        assert response["Content-Type"].startswith("text/csv")
        assert "Иван" in response.content.decode("utf-8-sig")
