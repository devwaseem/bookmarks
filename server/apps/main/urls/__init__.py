from django.urls import path, re_path

from server.apps.main.views.explore.views import (
    ArchiveBookmarkWidget,
    DeleteBookmarkWidget,
    EditBookmarkModalWidget,
    ExploreView,
)
from server.apps.main.views.add_bookmark.view import AddBookmarkView
from server.apps.main.views.widgets.add_new_bookmark.view import (
    AddBookmarkLinkAssistWidgetview,
    AddBookmarkModalWidgetView,
    AddBookmarkWidgetSearchCollectionsWidgetView,
)

app_name = "main"

widget_urlpatterns = [
    path(
        "widget/bookmark",
        AddBookmarkModalWidgetView.as_view(),
        name="widget-add-bookmark",
    ),
    path(
        "widget/bookmark/edit/<uuid:bookmark_id>",
        EditBookmarkModalWidget.as_view(),
        name="widget-edit-bookmark",
    ),
    path(
        "widget/bookmark/assist",
        AddBookmarkLinkAssistWidgetview.as_view(),
        name="widget-add-bookmark-assist",
    ),
    path(
        "widget/bookmark/tags/search",
        AddBookmarkWidgetSearchCollectionsWidgetView.as_view(),
        name="widget-add-bookmark-search-tags",
    ),
]

urlpatterns = [
    *widget_urlpatterns,
    re_path(
        r"(?P<link>^((https?:\/\/)?((\w+\.)?\w+\.\w+)|([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+))(\/.*)?$)",
        AddBookmarkView.as_view(),
        name="add-bookmark",
    ),
    path("", AddBookmarkView.as_view(), name="add-bookmark"),
    path("explore/", ExploreView.as_view(), name="explore"),
    path("explore/<str:collection>", ExploreView.as_view(), name="explore-collection"),
    path(
        "explore/widgets/archive_bookmark/<uuid:bookmark_id>",
        ArchiveBookmarkWidget.as_view(),
        name="explore-widget-archive-bookmark",
    ),
    path(
        "explore/widgets/delete_bookmark/<uuid:bookmark_id>",
        DeleteBookmarkWidget.as_view(),
        name="explore-widget-delete-bookmark",
    ),
]
