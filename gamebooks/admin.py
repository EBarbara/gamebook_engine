from django.contrib import admin

from .models import Gamebook, Paragraph, ReadingSession

admin.site.register(Gamebook)
admin.site.register(ReadingSession)

@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    ordering = ['gamebook__code', 'number']
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }