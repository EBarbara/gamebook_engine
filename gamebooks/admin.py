from django.contrib import admin

from .models import Gamebook, Paragraph

admin.site.register(Gamebook)

@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }