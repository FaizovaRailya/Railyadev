"""Views ядра: главная, обо мне, контакты, обработчики ошибок."""

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from apps.portfolio.models import Project
from apps.reviews.models import Testimonial
from apps.services.models import Service, Skill

from .forms import ContactForm


def home(request):
    """Главная: услуги, избранные кейсы, отзывы."""
    context = {
        "services": Service.objects.filter(is_active=True)[:4],
        "projects": Project.objects.filter(is_published=True, is_featured=True)[:6],
        "testimonials": Testimonial.objects.filter(is_published=True)[:3],
    }
    return render(request, "core/home.html", context)


def about(request):
    """Обо мне: навыки по категориям."""
    skills = Skill.objects.all()
    # Группировка по категориям для шаблона
    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.get_category_display(), []).append(skill)
    return render(
        request,
        "core/about.html",
        {"skills_by_category": skills_by_category},
    )


def contact(request):
    """Форма заявки с rate limit по IP (не более 3 в час)."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ip = request.META.get("REMOTE_ADDR", "") or "unknown"
            cache_key = f"contact_rate:{ip}"
            count = cache.get(cache_key, 0)

            if count >= 3:
                messages.error(
                    request,
                    "Слишком много заявок с вашего IP. Попробуйте через час.",
                )
                return redirect("core:contact")

            obj = form.save(commit=False)
            obj.ip_address = ip if ip != "unknown" else None
            obj.user_agent = request.META.get("HTTP_USER_AGENT", "")[:1000]
            obj.save()

            cache.set(cache_key, count + 1, 3600)

            send_mail(
                subject="Новая заявка с сайта",
                message=(
                    f"Имя: {obj.name}\n"
                    f"Email: {obj.email}\n"
                    f"Телефон: {obj.phone}\n\n"
                    f"{obj.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            messages.success(request, "Заявка отправлена. Свяжусь с вами.")
            return redirect("core:contact")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})


def handler404(request, exception):
    """Кастомная страница 404."""
    return render(request, "404.html", status=404)


def handler500(request):
    """Кастомная страница 500."""
    return render(request, "500.html", status=500)
