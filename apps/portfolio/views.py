"""Views портфолио: список кейсов с фильтрами и пагинацией, страница кейса."""

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Project, Technology


def project_list(request):
    """Список кейсов с фильтром по технологии/категории и пагинацией 9 на страницу."""
    qs = Project.objects.filter(is_published=True)

    tech_slug = request.GET.get("technology", "").strip()
    category = request.GET.get("category", "").strip()

    if tech_slug:
        qs = qs.filter(technologies__slug=tech_slug)
    if category:
        qs = qs.filter(category=category)

    qs = qs.distinct().order_by("order", "-date")

    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "portfolio/list.html",
        {
            "page_obj": page_obj,
            "technologies": Technology.objects.all(),
            "categories": Project.Category.choices,
            "current_tech": tech_slug,
            "current_category": category,
        },
    )


def project_detail(request, slug):
    """Страница кейса."""
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, "portfolio/detail.html", {"project": project})
