"""Админка портфолио."""

from django.contrib import admin

from .models import Project, ProjectImage, Technology


class ProjectImageInline(admin.TabularInline):
    """Галерея кейса прямо на странице кейса."""

    model = ProjectImage
    extra = 1
    fields = ("image", "alt", "order")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_featured",
        "is_published",
        "date",
        "order",
    )
    list_filter = ("category", "is_featured", "is_published")
    search_fields = ("name", "short_description", "task", "solution", "result")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("technologies",)
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "short_description")}),
        ("Подробности", {"fields": ("task", "solution", "result")}),
        ("Стек и обложка", {"fields": ("technologies", "cover")}),
        ("Ссылки", {"fields": ("site_url", "repo_url")}),
        (
            "Метаданные",
            {
                "fields": ("date", "testimonial", "is_featured", "order", "is_published"),
            },
        ),
    )
