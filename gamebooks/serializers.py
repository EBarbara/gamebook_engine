# gamebooks/serializers.py
from rest_framework.serializers import ModelSerializer

from .models import Gamebook, Paragraph


class ParagraphSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['number', 'text', 'combat_enemy', 'combat_skill', 'combat_stamina']

class GamebookDetailsSerializer(ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Gamebook
        fields = ['code', 'title', 'paragraphs']

class GamebookListSerializer(ModelSerializer):
    class Meta:
        model = Gamebook
        fields = ['code', 'title']
