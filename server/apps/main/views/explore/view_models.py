from enum import StrEnum
from functools import cache
from typing import cast
from django.db.models import Count, QuerySet
from django.http.request import HttpRequest

from server.apps.main.models.bookmark import Bookmark, BookmarkCollection, LinkType
from server.apps.main.models.user import User


class SidebarViewModel:
    def __init__(self, request: HttpRequest, collection: str | None) -> None:
        self.request = request
        self.collection = collection
        self.user = cast(User, self.request.user)

    def collection_list(self):
        collections_qs = (
            BookmarkCollection.objects.filter(created_by=self.user)
            .annotate(bookmarks_count=Count("bookmarks"))
            .filter(bookmarks_count__gt=0)
            .order_by("name")
        )
        return collections_qs


class SortType(StrEnum):
    ASCENDING = "A - Z"
    DESCENDING = "Z - A"
    RECENTLY_ADDED = "Recently Added"


class ExploreViewModel:
    def __init__(
        self,
        request: HttpRequest,
        collection: str | None,
        selected_type: LinkType | None = None,
        selected_sort_type: SortType | None = None,
    ) -> None:
        self.request = request
        self.collection = collection
        self.user = cast(User, self.request.user)
        self.selected_type = selected_type
        self.selected_sort_type = selected_sort_type

    def is_collection_mode(self):
        return bool(self.collection)

    def bookmark_types_list(self):
        return list(LinkType)

    def bookmark_sort_types_list(self):
        return list(SortType)

    @property
    def _bookmarks_queryset(self) -> QuerySet[Bookmark]:
        queryset = Bookmark.objects.filter(created_by=self.user).order_by("-created_at")
        if self.selected_type:
            queryset = queryset.filter(link_type=self.selected_type)

        if self.selected_sort_type:
            match self.selected_sort_type:
                case SortType.ASCENDING:
                    queryset = queryset.order_by("title")
                case SortType.DESCENDING:
                    queryset = queryset.order_by("-title")
                case SortType.RECENTLY_ADDED:
                    queryset = queryset.order_by("-created_at")
        return queryset

    @cache
    def does_reading_list_bookmarks_exist(self) -> bool:
        return self.reading_list_bookmark_list().exists()

    @cache
    def does_collection_bookmarks_exist(self) -> bool:
        return self.collection_bookmark_list().exists()

    @cache
    def reading_list_bookmark_list(self) -> QuerySet[Bookmark]:
        if self.collection:
            return self._bookmarks_queryset.filter(
                collections__name=self.collection,
                archived=False,
            )
        return self._bookmarks_queryset.filter(archived=False)

    @cache
    def collection_bookmark_list(self) -> QuerySet[Bookmark]:
        return self._bookmarks_queryset.filter(
            collections__name=self.collection,
            archived=True,
        )

    def no_results_found(self) -> bool:
        return not (self.does_reading_list_bookmarks_exist() or self.does_collection_bookmarks_exist())
