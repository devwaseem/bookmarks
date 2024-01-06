from django.contrib import admin

from server.apps.main.models.bookmark import Bookmark, BookmarkCollection


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    ...


@admin.register(BookmarkCollection)
class BookmarkTagAdmin(admin.ModelAdmin):
    ...
