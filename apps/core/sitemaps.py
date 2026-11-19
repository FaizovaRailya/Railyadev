"""Sitemap-классы для всех публичных страниц."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import BlogPost
from apps.portfolio.models import Project
from apps.services.models import Service


class StaticSitemap(Sitemap):
    """Статические страницы."""

    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "core:contact",
            "core:privacy",
            "portfolio:list",
            "services:list",
            "blog:list",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    """Страницы кейсов."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    """Страницы услуг (все ведут на /services/#slug)."""

    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    """Опубликованные статьи."""

    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED).order_by("-published_at")

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticSitemap,
    "projects": ProjectSitemap,
    "services": ServiceSitemap,
    "blog": BlogSitemap,
}
