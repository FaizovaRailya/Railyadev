"""Базовые модели и модели ядра: настройки сайта, заявки."""

from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Абстрактная модель с created_at/updated_at."""

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    """Абстрактная модель с уникальным slug и автогенерацией из названия."""

    slug = models.SlugField("Slug", unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.get_slug_source(), allow_unicode=True)[:50] or "item"
            slug = base
            i = 2
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_slug_source(self) -> str:
        """Поле, из которого генерируется slug. Переопределяется при необходимости."""
        return getattr(self, "name", getattr(self, "title", ""))


class SiteSettings(TimeStampedModel):
    """Синглтон: глобальные настройки сайта. Одна запись на весь проект."""

    name = models.CharField("Имя/бренд", max_length=120)
    slogan = models.CharField("Слоган", max_length=255, blank=True)
    avatar = models.ImageField("Аватар", upload_to="site/", blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    telegram = models.URLField("Telegram", blank=True)
    whatsapp = models.URLField("WhatsApp", blank=True)
    max_url = models.URLField("MAX", blank=True)
    github = models.URLField("GitHub", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    postal_address = models.CharField("Почтовый адрес", max_length=255, blank=True)
    timezone = models.CharField("Часовой пояс", max_length=64, default="Europe/Moscow")
    meta_title = models.CharField("Meta title", max_length=255, blank=True)
    meta_description = models.TextField("Meta description", blank=True)
    og_image = models.ImageField("OG image", upload_to="site/", blank=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        if SiteSettings.objects.filter(pk=1).exists():
            # Сохранить created_at от существующей записи — иначе UPDATE затрёт его в NULL
            existing = SiteSettings.objects.only("created_at").get(pk=1)
            self.created_at = existing.created_at
            kwargs.pop("force_insert", None)
            kwargs["force_update"] = True
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Вернуть единственную запись, создав дефолтную при необходимости."""
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"name": "Портфолио"})
        return obj


class ContactRequest(TimeStampedModel):
    """Заявка с формы контактов."""

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Завершена"
        SPAM = "spam", "Спам"

    name = models.CharField("Имя", max_length=120)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=32, blank=True)
    message = models.TextField("Сообщение")
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    ip_address = models.GenericIPAddressField("IP", null=True, blank=True)
    user_agent = models.TextField("User-Agent", blank=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
