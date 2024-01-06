from typing import cast
from uuid import UUID
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django_htmx.http import HttpResponseClientRefresh
from render_block import render_block_to_string
import structlog
from server.apps.main.forms.bookmarks import AddBookmarkWidgetForm, ArchiveBookmarkWidgetForm
from server.apps.main.helpers.htmx import HTMXLoginRequiredMixin, ToastType, htmx_show_toast
from server.apps.main.models.bookmark import Bookmark, BookmarkCollection, LinkType
from server.apps.main.models.user import User
from server.apps.main.services.bookmark import update_bookmark

from server.apps.main.views.explore.view_models import ExploreViewModel, SidebarViewModel, SortType


logger = structlog.get_logger(__name__)


class ExploreView(LoginRequiredMixin, View):
    template_name = "main/templates/explore/index.html"

    def get(self, request: HttpRequest, collection: str | None = None):
        if collection:
            does_collection_exists = BookmarkCollection.objects.filter(
                created_by=cast(User, self.request.user),
                name=collection,
            ).exists()
            if not does_collection_exists:
                raise Http404()

        selected_type: LinkType | None = None
        if _selected_type := request.GET.get("type", None):
            try:
                selected_type = LinkType(_selected_type)
            except Exception:
                return HttpResponseBadRequest("Invalid type")

        selected_sort_type: SortType | None = None
        if _selected_sort_type := request.GET.get("sort", None):
            try:
                selected_sort_type = SortType(_selected_sort_type)
            except Exception:
                return HttpResponseBadRequest("Invalid sort")

        context = {
            "sidebar_view_model": SidebarViewModel(
                request=request,
                collection=collection,
            ),
            "explore_view_model": ExploreViewModel(
                request=request,
                collection=collection,
                selected_type=selected_type,
                selected_sort_type=selected_sort_type,
            ),
        }
        if request.htmx and not request.htmx.boosted:  # type: ignore
            return HttpResponse(
                render_block_to_string(
                    request=request,
                    template_name=self.template_name,
                    block_name="main",
                    context=context,
                )
            )

        return render(
            request=request,
            template_name=self.template_name,
            context=context,
        )


class ArchiveBookmarkWidget(HTMXLoginRequiredMixin, View):
    def post(self, request: HttpRequest, bookmark_id: UUID):
        bookmark = get_object_or_404(
            Bookmark,
            created_by=self.request.user,
            id=bookmark_id,
        )
        form = ArchiveBookmarkWidgetForm(request.POST)
        if not form.is_valid():
            breakpoint()
            response = HttpResponse("", status=400)
            logger.error(form.errors)
            return response
        should_archive = form.cleaned_data["archive_bookmark"]
        bookmark.archived = should_archive
        bookmark.save()
        return HttpResponseClientRefresh()


class EditBookmarkModalWidget(HTMXLoginRequiredMixin, View):
    template_name = "main/templates/widgets/add_new_bookmark_modal/index.html"

    def get(self, request: HttpRequest, bookmark_id: UUID):
        bookmark = get_object_or_404(
            Bookmark,
            created_by=self.request.user,
            id=bookmark_id,
        )

        form = AddBookmarkWidgetForm(
            initial={
                "link": bookmark.link,
                "title": bookmark.title,
                "link_type": bookmark.link_type,
                "add_to_reading_list": not bookmark.archived,
            }
        )

        return render(
            request=request,
            template_name=self.template_name,
            context={"form": form},
        )

    def post(self, request: HttpRequest, bookmark_id: UUID):
        bookmark = get_object_or_404(
            Bookmark,
            created_by=self.request.user,
            id=bookmark_id,
        )

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

        update_bookmark(
            bookmark=bookmark,
            user=user,
            link=link,
            link_type=link_type,
            title=title,
            add_to_reading_list=add_to_reading_list,
            collections=collections,
        )

        response = HttpResponse(status=204)
        htmx_show_toast(
            response=response,
            message="Bookmark Saved",
            type=ToastType.SUCCESS,
        )
        return response


class DeleteBookmarkWidget(HTMXLoginRequiredMixin, View):
    def post(self, request: HttpRequest, bookmark_id: UUID):
        bookmark = get_object_or_404(
            Bookmark,
            created_by=self.request.user,
            id=bookmark_id,
        )
        bookmark.delete()
        return HttpResponseClientRefresh()
