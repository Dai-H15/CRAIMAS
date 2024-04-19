from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_item(value, key):
    if isinstance(value, dict):
        return value.get(key)
    else:
        return getattr(value, key, None)


@register.simple_tag
def get_interview(value, sets):
    if sets[value] is not None:
        return mark_safe(f"<button class='btn btn-outline-info' onclick='open_as_window(\"{reverse('view_interview', args=[str(sets[value])])}\", \"interview\", 500, 800)'> 開く</button>")
    else:
        return mark_safe("<p>未登録</p>")
