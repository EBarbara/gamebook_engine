# gamebooks/views.py
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Gamebook, Paragraph
from .serializers import ParagraphSerializer, GamebookListSerializer, GamebookDetailsSerializer


class GamebookViewSet(ModelViewSet):
    queryset = Gamebook.objects.all()
    lookup_field = 'code'

    def get_serializer_class(self):
        if self.action == 'list':
            return GamebookListSerializer
        return GamebookDetailsSerializer


class ParagraphViewSet(ModelViewSet):
    serializer_class = ParagraphSerializer
    lookup_field = 'number'

    def get_queryset(self):
        book_code = self.kwargs.get('gamebook_code')
        book = get_object_or_404(Gamebook, code=book_code)
        return Paragraph.objects.filter(gamebook=book)

    def perform_create(self, serializer):
        book_code = self.kwargs.get('gamebook_code')
        book = get_object_or_404(Gamebook, code=book_code)
        serializer.save(gamebook=book)