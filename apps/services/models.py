"""Модели услуг и навыков."""

from django.db import models
from django.urls import reverse

from apps.core.models import SlugMixin, TimeStampedModel


class Skill(TimeStampedModel):
    """Навык для блока «Обо мне»."""

    class Category(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DEVOPS = "devops", "DevOps"
        TOOLS = "tools", "Инструменты"

    name = models.CharField("Название", max_length=100)
    level = models.PositiveSmallIntegerField("Уровень", default=0)
    category = models.CharField("Категория", max_length=20, choices=Category.choices)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.level}%)"


class Service(SlugMixin, TimeStampedModel):
    """Услуга с ценой и сроком."""

    name = models.CharField("Название", max_length=150)
    short_description = models.TextField("Краткое описание")
    full_description = models.TextField("Полное описание")
    price_from = models.DecimalField(
        "Цена от",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    duration = models.CharField("Срок", max_length=100, blank=True)
    icon = models.CharField("Иконка bootstrap-icons", max_length=80, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Отдельной страницы услуги нет — ведём на список с якорем.
        return f"{reverse('services:list')}#{self.slug}"
