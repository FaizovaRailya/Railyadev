"""URLs портфолио."""

from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("<str:slug>/", views.project_detail, name="detail"),  # было <slug:slug>
]
