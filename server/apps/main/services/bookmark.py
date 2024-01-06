from django.db import transaction
from server.apps.main.models.bookmark import Bookmark, BookmarkCollection, LinkType
from server.apps.main.models.user import User


def create_bookmark(
    *,
    user: User,
    link: str,
    link_type: LinkType,
    title: str,
    add_to_reading_list: bool,
    collections: list[str],
):
    with transaction.atomic():
        BookmarkCollection.objects.bulk_create(
            [BookmarkCollection(created_by=user, name=collection) for collection in collections],
            ignore_conflicts=True,
        )

        new_bookmark = Bookmark(
            created_by=user,
            title=title,
            link_type=link_type,
            link=link,
            archived=not add_to_reading_list,
        )
        new_bookmark.save()
        new_bookmark.collections.set(
            BookmarkCollection.objects.filter(
                created_by=user,
                name__in=collections,
            )
        )


def update_bookmark(
    *,
    bookmark: Bookmark,
    user: User,
    link: str,
    link_type: LinkType,
    title: str,
    add_to_reading_list: bool,
    collections: list[str],
):
    with transaction.atomic():
        BookmarkCollection.objects.bulk_create(
            [BookmarkCollection(created_by=user, name=collection) for collection in collections],
            ignore_conflicts=True,
        )

        bookmark.title = title
        bookmark.link_type = link_type
        bookmark.link = link
        bookmark.archived = not add_to_reading_list

        bookmark.save()
        bookmark.collections.set(
            BookmarkCollection.objects.filter(
                created_by=user,
                name__in=collections,
            )
        )
