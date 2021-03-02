from django.template import Library
from phonenumbers import format_number


register = Library()

@register.filter
def format_phone(phone):
    return format_number(phone, 2)
