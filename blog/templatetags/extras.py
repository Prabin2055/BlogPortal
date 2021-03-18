from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)