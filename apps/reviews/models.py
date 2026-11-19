"""Модель отзывов клиентов."""

from django.db import models

from apps.core.models import TimeStampedModel


class Testimonial(TimeStampedModel):
    """Отзыв клиента."""

    name = models.CharField("Имя", max_length=120)
    company = models.CharField("Компания", max_length=150, blank=True)
    position = models.CharField("Должность", max_length=150, blank=True)
    text = models.TextField("Текст")
    photo = models.ImageField("Фото", upload_to="reviews/", blank=True)
    rating = models.PositiveSmallIntegerField("Рейтинг", default=5)
    date = models.DateField("Дата")
    is_published = models.BooleanField("Опубликован", default=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.name} — {self.rating}/5"
