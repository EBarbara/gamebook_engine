# gamebooks/views.py
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Gamebook, Paragraph, ReadingSession
from .serializers import (
    ParagraphSerializer, GamebookListSerializer, GamebookDetailsSerializer, ReadingSessionSerializer
)
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

class ReadingSessionViewSet(ModelViewSet):
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_paragraph_number = request.data.get('current_paragraph')

        if new_paragraph_number is not None:
            try:
                # Busca o Paragraph certo com base no book da sessão + número
                paragraph = Paragraph.objects.get(gamebook=instance.book, number=new_paragraph_number)
            except Paragraph.DoesNotExist:
                return Response(
                    {"detail": f"Parágrafo número {new_paragraph_number} não encontrado para este livro."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Atualiza o histórico
            if instance.current_paragraph:
                instance.history.append(instance.current_paragraph.number)

            instance.current_paragraph = paragraph
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def gamebook_graph(request, code):
    book = get_object_or_404(Gamebook, code=code)
    graph = build_paragraph_graph(book)
    return Response(graph, status=status.HTTP_200_OK)
