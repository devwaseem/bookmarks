from django import template
from django.utils.html import escape

from server.apps.main.helpers.string import mark_as_strong_for

register = template.Library()


@register.filter(is_safe=True)
def bold_for(value, arg):
    """
    Make a part of text bold.

    Use `{{ "text_part_example"|bold_for:"example" }}`
    """
    return mark_as_strong_for(escape(value), escape(arg))
