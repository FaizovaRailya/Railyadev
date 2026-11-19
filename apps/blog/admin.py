"""Админка блога."""

from django.contrib import admin

from .models import BlogPost, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "status",
        "published_at",
        "is_featured",
        "created_at",
    )
    list_filter = ("status", "is_featured", "tags")
    search_fields = ("title", "short_description", "text")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "status")}),
        ("Контент", {"fields": ("short_description", "text", "cover", "tags")}),
        (
            "Публикация",
            {
                "fields": ("published_at", "is_featured"),
            },
        ),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
    )
