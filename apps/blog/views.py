"""Views блога: список статей, страница статьи, поиск."""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import BlogPost


def blog_list(request):
    """Список опубликованных статей с поиском и пагинацией 9 на страницу."""
    qs = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(text__icontains=q))

    qs = qs.order_by("-published_at", "-created_at")

    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/list.html",
        {"page_obj": page_obj, "q": q},
    )


def blog_detail(request, slug):
    """Страница статьи."""
    post = get_object_or_404(
        BlogPost,
        slug=slug,
        status=BlogPost.Status.PUBLISHED,
    )
    return render(request, "blog/detail.html", {"post": post})
