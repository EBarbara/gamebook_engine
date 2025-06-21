# gamebooks/views.py
from rest_framework.viewsets import ModelViewSet

from .models import Gamebook, Paragraph
from .serializers import GamebookSerializer, ParagraphSerializer


class GamebookViewSet(ModelViewSet):
    queryset = Gamebook.objects.all()
    serializer_class = GamebookSerializer
    lookup_field = 'code'


class ParagraphViewSet(ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer