"""Контекст-процессоры для всех шаблонов."""

from .models import SiteSettings


def site_settings(request):
    """Добавляет site_settings во все шаблоны."""
    return {"site_settings": SiteSettings.load()}
