from typing import TypeVar

from django.db.models import Model

T = TypeVar("T", bound=Model)


def get_object_or_none(classmodel: type[T], **kwargs) -> T | None:
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
