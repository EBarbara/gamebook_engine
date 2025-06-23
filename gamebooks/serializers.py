# gamebooks/serializers.py
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Gamebook, Paragraph, ReadingSession
from .templatetags import gamebook_filters


class ParagraphSerializer(ModelSerializer):
    rendered_text = SerializerMethodField()

    class Meta:
        model = Paragraph
        fields = ['number', 'text', 'rendered_text']

    def get_rendered_text(self, obj):
        return gamebook_filters.render_gamebook_links(obj.text, obj.gamebook.code)

class GamebookDetailsSerializer(ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Gamebook
        fields = ['code', 'title', 'paragraphs']

class GamebookListSerializer(ModelSerializer):
    class Meta:
        model = Gamebook
        fields = ['code', 'title']

class ReadingSessionSerializer(ModelSerializer):
    current_paragraph_number = IntegerField(source='current_paragraph.number', read_only=True)

    class Meta:
        model = ReadingSession
        fields = ['id', 'book', 'current_paragraph', 'current_paragraph_number', 'created_at', 'updated_at', 'state']