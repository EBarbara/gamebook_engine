# gamebooks/models.py
from django.db import models

class Gamebook (models.Model):
    code = models.SlugField(unique=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Paragraph (models.Model):
    gamebook = models.ForeignKey(Gamebook, on_delete=models.CASCADE, related_name='paragraphs')
    number = models.IntegerField()
    text = models.TextField()
    combat_enemy = models.CharField(max_length=100, null=True, blank=True)
    combat_skill = models.IntegerField(null=True, blank=True)
    combat_stamina = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('gamebook', 'number')

class Choice (models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField(max_length=300)
    target = models.IntegerField()
