# gamebooks/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Gamebook, Paragraph
from .serializers import ParagraphSerializer, GamebookListSerializer, GamebookDetailsSerializer
from .utils import build_paragraph_graph


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

@api_view(['GET'])
def gamebook_graph(request, code):
    book = get_object_or_404(Gamebook, code=code)
    graph = build_paragraph_graph(book)
    return Response(graph, status=status.HTTP_200_OK)
