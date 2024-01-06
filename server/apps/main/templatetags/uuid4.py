import uuid

from django import template

register = template.Library()


@register.filter
def uuid4(value):
    """
    generate random filter.

    Use `{{ "uuid4"|uuid4 }}`
    """
    return value.replace("uuid4", str(uuid.uuid4()))
