from typing import cast
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic import View
from render_block import render_block_to_string
import structlog
from server.apps.main.forms.bookmarks import AddBookmarkWidgetForm

from server.apps.main.helpers.htmx import (
    HTMXLoginRequiredMixin,
    ToastType,
    htmx_show_toast,
)
from server.apps.main.helpers.url import is_valid_url
from server.apps.main.models.bookmark import BookmarkCollection, LinkType
from server.apps.main.models.user import User
from server.apps.main.services.bookmark import create_bookmark
from server.apps.main.services.url import extract_title_from_url, guess_link_type

logger = structlog.get_logger(__name__)


class AddBookmarkModalWidgetView(HTMXLoginRequiredMixin, View):
    template_name = "main/templates/widgets/add_new_bookmark_modal/index.html"

    def get(self, request: HttpRequest):
        return render(
            request=request,
            template_name=self.template_name,
            context={"form": AddBookmarkWidgetForm},
        )

    def post(self, request: HttpRequest):
        user = cast(User, request.user)
        form = AddBookmarkWidgetForm(request.POST)
        context = {
            "form": form,
        }
        if not form.is_valid():
            return render(
                request=request,
                template_name=self.template_name,
                context=context,
            )

        form_data = form.cleaned_data
        collections = form_data["collections"]
        title = form_data["title"]
        link = form_data["link"]
        link_type = LinkType(form_data["link_type"])
        add_to_reading_list = form_data["add_to_reading_list"]

        create_bookmark(
            user=user,
            link=link,
            link_type=link_type,
            title=title,
            add_to_reading_list=add_to_reading_list,
            collections=collections,
        )

        response = HttpResponse(status=201)
        htmx_show_toast(
            response=response,
            message="Bookmark Added",
            type=ToastType.SUCCESS,
        )
        return response


class AddBookmarkLinkAssistWidgetview(HTMXLoginRequiredMixin, View):
    template_name = "main/components/add_bookmark/form_content.html"

    def get(self, request):
        form = AddBookmarkWidgetForm(initial=request.GET)
        if link := form.initial.get("link"):
            if is_valid_url(link):
                title = extract_title_from_url(link)
                link_type = guess_link_type(link)
                form = AddBookmarkWidgetForm(
                    initial={
                        "link": link,
                        "title": title,
                        "link_type": link_type,
                    }
                )
            else:
                logger.warning(f"Invalid Link: {link}")

        return HttpResponse(
            render_block_to_string(
                request=request,
                template_name=self.template_name,
                block_name="add_bookmark_assist",
                context={"form": form},
            )
        )


class AddBookmarkWidgetSearchCollectionsWidgetView(HTMXLoginRequiredMixin, View):
    template_name = "main/components/add_bookmark/collections_search_results.html"

    def get(self, request: HttpRequest):
        user = cast(User, request.user)
        query = request.GET.get("query")
        bookmark_tags_qs = None
        found_exact_match = False
        if query:
            bookmark_tags_qs = BookmarkCollection.objects.filter(
                created_by=user,
                name__icontains=query,
            )
            found_exact_match = BookmarkCollection.objects.filter(
                created_by=user,
                name__iexact=query,
            ).exists()
        context = {
            "query": query,
            "bookmark_tags": bookmark_tags_qs,
            "found_exact_match": found_exact_match,
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context,
        )
