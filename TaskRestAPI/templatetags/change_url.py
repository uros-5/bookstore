from urllib.parse import quote_plus
from django import template

register = template.Library()


@register.filter
def change_url(value, idd=0):
	if (idd == 0):
		return value.replace('/', "")
	elif (idd == 1):
		return (value.replace("/", "").replace(" ", "_").lower() + "_id")
