import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def render_gamebook_links(text, book_code):
    """
    Substitui placeholders do tipo [[paragraph:123]] por links reais.
    """
    def replace(match):
        target = match.group(1)
        return f'<a href="#" onclick="gotoParagraph({target}); return false;">{target}</a>'

    result = re.sub(r'\[\[paragraph:(\d+)\]\]', replace, text)
    return mark_safe(result)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])