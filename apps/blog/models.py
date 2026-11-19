"""Модели блога: теги и статьи."""

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.core.models import SlugMixin, TimeStampedModel


class Tag(TimeStampedModel):
    """Тег статьи."""

    name = models.CharField("Название", max_length=80)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(SlugMixin, TimeStampedModel):
    """Статья блога."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"

    title = models.CharField("Заголовок", max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.PROTECT,
    )
    short_description = models.TextField("Краткое описание")
    text = models.TextField("Текст")
    cover = models.ImageField("Обложка", upload_to="blog/", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)
    meta_title = models.CharField("Meta title", max_length=255, blank=True)
    meta_description = models.TextField("Meta description", blank=True)
    is_featured = models.BooleanField("Избранная", default=False)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_slug_source(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
