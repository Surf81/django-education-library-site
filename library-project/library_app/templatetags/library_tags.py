from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='getattr')
def getattrfilter(o, attr: str):
    try:
        return getattr(o, attr)
    except:
        return settings.TEMPLATE_STRING_IF_INVALID


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()        