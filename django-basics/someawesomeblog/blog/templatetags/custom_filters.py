import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

url_pattern = re.compile(r'(https?://[^\s]+)')
hashtag_pattern = re.compile(r'#(\w+)')

@register.filter(name='process_links')
def process_links(value):
    value = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', value)
    return mark_safe(value)

@register.filter(name='process_hashtags')
def process_links(value):
    value = hashtag_pattern.sub(r'<a href="/hashtag/\1">#\1</a>', value)
    return mark_safe(value)
