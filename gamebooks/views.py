# gamebooks/views.py
from rest_framework.viewsets import ModelViewSet

from .models import Gamebook
from .serializers import GamebookSerializer

class GamebookViewSet(ModelViewSet):
    queryset = Gamebook.objects.all()
    serializer_class = GamebookSerializer