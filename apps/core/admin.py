"""Админка ядра: SiteSettings (singleton), ContactRequest (только чтение + CSV)."""

import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import ContactRequest, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Singleton: запрет на добавление второй записи."""

    def has_add_permission(self, request):
        # Разрешаем добавить, только если записей ещё нет.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Удалять настройки нельзя — иначе нечего будет показывать в шаблонах.
        return False


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = (
        "name",
        "email",
        "phone",
        "message",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )
    fields = readonly_fields + ("status",)
    actions = ["export_csv"]
    date_hierarchy = "created_at"

    @admin.action(description="Экспорт в CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = 'attachment; filename="contact_requests.csv"'
        writer = csv.writer(response)
        writer.writerow(["Имя", "Email", "Телефон", "Сообщение", "Статус", "IP", "Создано"])
        for obj in queryset:
            writer.writerow(
                [
                    obj.name,
                    obj.email,
                    obj.phone,
                    obj.message,
                    obj.get_status_display(),
                    obj.ip_address or "",
                    obj.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
        return response
