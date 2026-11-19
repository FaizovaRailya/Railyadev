"""Админка услуг и навыков."""

from django.contrib import admin

from .models import Service, Skill


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price_from", "duration", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("name", "short_description", "full_description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "order")
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("category", "order")
