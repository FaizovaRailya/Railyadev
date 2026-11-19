"""
Корневой URL-конфиг проекта.

Подключает:
- /admin/         — Django Admin
- /              — apps.core (главная, обо мне, контакты, privacy)
- /portfolio/    — apps.portfolio (кейсы)
- /services/     — apps.services (услуги)
- /blog/         — apps.blog (статьи)
- /sitemap.xml   — sitemap
- /robots.txt    — robots.txt
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("portfolio/", include("apps.portfolio.urls")),
    path("services/", include("apps.services.urls")),
    path("blog/", include("apps.blog.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
]

# В dev-режиме Django сам раздаёт медиа-файлы.
# В проде этим занимается nginx (вне scope ТЗ).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Кастомные обработчики ошибок
handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"
