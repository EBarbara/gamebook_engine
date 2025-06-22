import re

from django import template

from django.urls import reverse

register = template.Library()


@register.filter
def render_gamebook_links(text, book_code):
    """
    Substitui placeholders do tipo [[paragraph:123]] por links reais.
    """

    def replace(match):
        number = match.group(1)
        url = reverse('read-paragraph', args=[book_code, number])
        return f'<a href="{url}">{number}</a>'

    return re.sub(r'\[\[paragraph:(\d+)\]\]', replace, text) # noinspection PyRedundantEscape

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])