# gamebooks/models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Gamebook (models.Model):
    code = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Paragraph (models.Model):
    gamebook = models.ForeignKey(Gamebook, on_delete=models.CASCADE, related_name='paragraphs')
    number = models.IntegerField()
    text = CKEditor5Field("Texto do Parágrafo", config_name="default")
    combat_enemy = models.CharField(max_length=100, null=True, blank=True)
    combat_skill = models.IntegerField(null=True, blank=True)
    combat_stamina = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('gamebook', 'number')

    def __str__(self):
        return f'{self.gamebook.title} - {self.number}'
