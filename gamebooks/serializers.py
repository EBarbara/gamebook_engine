# gamebooks/serializers.py
from rest_framework.serializers import ModelSerializer

from .models import Gamebook, Paragraph, Choice


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'target']


class ParagraphSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['number', 'text', 'combat_enemy', 'combat_skill', 'combat_stamina']


class GamebookSerializer(ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Gamebook
        fields = ['code', 'title']


