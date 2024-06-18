from django import template

register = template.Library()


@register.filter
def is_bigger(val1, val2):
    if val1 > val2:
        return True
    return False
