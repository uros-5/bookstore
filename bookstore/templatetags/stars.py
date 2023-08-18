from urllib.parse import quote_plus
from django import template
from bookstore.models import StavkeNarudzbine
from django.db.models import Sum

register = template.Library()


@register.filter
def star(n: int) -> str:
    s = ""
    for i in range(int(n)):
        s += "a"
    return s
