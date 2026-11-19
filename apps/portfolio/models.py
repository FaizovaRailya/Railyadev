"""Модели портфолио: технологии, кейсы, изображения кейсов."""

from django.db import models
from django.urls import reverse

from apps.core.models import SlugMixin, TimeStampedModel
from apps.reviews.models import Testimonial


class Technology(TimeStampedModel):
    """Технология из стека проектов."""

    name = models.CharField("Название", max_length=80)
    slug = models.SlugField("Slug", unique=True)
    icon = models.CharField("Иконка", max_length=80, blank=True)

    class Meta:
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(SlugMixin, TimeStampedModel):
    """Кейс в портфолио."""

    class Category(models.TextChoices):
        LANDING = "landing", "Лендинг"
        CORPORATE = "corporate", "Корпоративный"
        ECOMMERCE = "ecommerce", "E-commerce"
        API = "api", "API"
        OTHER = "other", "Другое"

    name = models.CharField("Название", max_length=200)
    category = models.CharField("Категория", max_length=20, choices=Category.choices)
    short_description = models.TextField("Краткое описание")
    task = models.TextField("Задача")
    solution = models.TextField("Решение")
    result = models.TextField("Результат")
    technologies = models.ManyToManyField(
        Technology,
        verbose_name="Стек",
        related_name="projects",
        blank=True,
    )
    cover = models.ImageField("Обложка", upload_to="projects/")
    site_url = models.URLField("Ссылка на сайт", blank=True)
    repo_url = models.URLField("Ссылка на репозиторий", blank=True)
    date = models.DateField("Дата")
    is_featured = models.BooleanField("Избранный", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Опубликован", default=True)
    testimonial = models.ForeignKey(
        Testimonial,
        verbose_name="Отзыв клиента",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"
        ordering = ["order", "-date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("portfolio:detail", kwargs={"slug": self.slug})


class ProjectImage(TimeStampedModel):
    """Изображение галереи кейса."""

    project = models.ForeignKey(
        Project,
        verbose_name="Кейс",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField("Изображение", upload_to="projects/gallery/")
    alt = models.CharField("Alt", max_length=255, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Изображение кейса"
        verbose_name_plural = "Изображения кейса"
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.name} — {self.alt or self.pk}"
