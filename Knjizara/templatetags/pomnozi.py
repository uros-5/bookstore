from urllib.parse import quote_plus
from django import template

register = template.Library()


@register.filter
def pomnozi(value1,value2):
    return round(value1*value2,2)
