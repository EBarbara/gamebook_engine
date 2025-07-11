# gamebooks/models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Gamebook (models.Model):
    code = models.SlugField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Paragraph (models.Model):
    gamebook = models.ForeignKey(Gamebook, on_delete=models.CASCADE, related_name='paragraphs')
    number = models.IntegerField()
    text = CKEditor5Field("Texto do Parágrafo", config_name="default")
    events = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ('gamebook', 'number')

    def __str__(self):
        return f'{self.gamebook.title} - {self.number}'

class ReadingSession (models.Model):
    book = models.ForeignKey(Gamebook, on_delete=models.CASCADE, related_name='sessions')
    current_paragraph = models.ForeignKey(Paragraph, on_delete=models.SET_NULL, null=True, blank=True)
    history = models.JSONField(default=list)
    state = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session for {self.book.title} at paragraph {self.current_paragraph.number if self.current_paragraph else 'None'}"

class ReadingSessionState(models.Model):
    session = models.ForeignKey(ReadingSession, on_delete=models.CASCADE, related_name='state_snapshots')
    created_at = models.DateTimeField(auto_now_add=True)
    paragraph_number = models.IntegerField()
    state = models.JSONField(default=dict)

    class Meta:
        ordering = ['created_at']
