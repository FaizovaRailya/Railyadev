"""Views услуг."""

from django.shortcuts import render

from .models import Service


def service_list(request):
    """Список активных услуг."""
    return render(
        request,
        "services/list.html",
        {"services": Service.objects.filter(is_active=True)},
    )
