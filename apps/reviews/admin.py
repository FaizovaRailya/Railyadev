"""Админка отзывов."""

from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "rating", "date", "is_published")
    list_filter = ("rating", "is_published")
    search_fields = ("name", "company", "text")
    date_hierarchy = "date"
