import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

url_pattern = re.compile(r'(https?://[^\s]+)')

@register.filter(name='process_links')
def process_links(value):
    value = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', value)
    return mark_safe(value)
