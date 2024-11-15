from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from urllib.parse import urlparse

register = template.Library()


def is_url(value):
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False


@register.filter
def get_item(value, key):
    if isinstance(value, dict):
        res = value.get(key)
    else:
        res = getattr(value, key, None)
    if is_url(res):
        return mark_safe(f"<p>{(res[:20] + '...')if len(res) >= 20 else res}</p><button class='btn btn-outline-info' onclick='Main.default.open_as_window.open_as_window(\"{res}\", \"URL\", 1200, 1000)'> ページを開く</button>")
    return res


@register.simple_tag
def get_interview(value, sets):
    if sets[value] is not None:
        return mark_safe(f"<button class='btn btn-outline-info' onclick='Main.default.open_as_window.open_as_window(\"{reverse('view_interview', args=[str(sets[value])])}\", \"interview\", 560, 1000)'> 開く</button>")
    else:
        return mark_safe("<p>未登録</p>")
