import re
from django.db import models
from server.apps.main.models.base import BaseUUIDModel, TimestampedModel
from server.apps.main.models.user import User


class BookmarkCollection(TimestampedModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="bookmark_collections",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bookmark Collection"
        verbose_name_plural = "Bookmark Collections"
        ordering = ["name"]
        unique_together = ("created_by", "name")
        indexes = [
            models.Index(
                fields=["created_by", "name"],
                name="created_by__name__idx",
            ),
        ]


class LinkType(models.TextChoices):
    ARTICLE = "ARTICLE", "Article"
    VIDEO = "VIDEO", "Video"
    SOCIAL_POST = "SOCIAL_POST", "Social Post"
    LINK = "LINK", "Link"
    EMAIL = "EMAIL", "Email"
    PERSON = "PERSON", "Person"


class Bookmark(TimestampedModel, BaseUUIDModel):
    class Status(models.TextChoices):
        ADDED = "ADDED", "Added"
        VISITED = "VISITED", "Visited"
        READ = "READ", "Read"

    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    description = models.TextField()
    link_type = models.CharField(max_length=100, choices=LinkType.choices)
    link = models.URLField(max_length=255)
    collections = models.ManyToManyField(BookmarkCollection, related_name="bookmarks")
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def short_link(self):
        groups = re.search(r"https?://(?:www\.)?([^/]+)", self.link)
        if groups:
            return groups[1]
        return self.link

    def feather_icon(self):
        match self.link_type:
            case LinkType.ARTICLE:
                return "book"
            case LinkType.VIDEO:
                return "video"
            case LinkType.SOCIAL_POST:
                return "radio"
            case LinkType.LINK:
                return "link"
            case LinkType.EMAIL:
                return "mail"
            case LinkType.PERSON:
                return "user"
