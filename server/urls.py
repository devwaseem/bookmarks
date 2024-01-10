"""
URL Configuration for Bookmarks

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static  # noqa: WPS433
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import include, path
from django.views.generic import TemplateView
from django_ratelimit.exceptions import Ratelimited

from server.apps.main import urls as main_urls


def not_found(_):
    return HttpResponseNotFound()


def handler404(request: HttpRequest, *args, **kwargs) -> HttpResponse:  # noqa
    return render(request, "errors/404.html", status=404)


def handler403(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:  # noqa
    if isinstance(exception, Ratelimited):
        return HttpResponse("Sorry you are blocked", status=429)
    return render(request, "errors/403.html", status=403)


def handler500(request: HttpRequest, *args, **kwargs) -> HttpResponse:  # noqa
    return render(request, "errors/500.html", status=500)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/email/", handler404),
    path("", include("allauth.urls")),  # django allauth urls
    path("", include(main_urls)),
    # Text and xml static files:
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="txt/robots.txt",
            content_type="text/plain",
        ),
    ),
    path(
        "humans.txt",
        TemplateView.as_view(
            template_name="txt/humans.txt",
            content_type="text/plain",
        ),
    ),
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433

    urlpatterns = [
        # Django silk
        # path("silk/", include("silk.urls", namespace="silk")),
        path("__reload__/", include("django_browser_reload.urls")),
        # URLs specific only to django-debug-toolbar:
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
        # Serving media files in development only:
        *static(  # noqa
            settings.STATIC_URL,  # type: ignore
            document_root=settings.STATIC_ROOT,
        ),
        *static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        ),
    ]
