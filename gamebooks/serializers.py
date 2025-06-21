# gamebooks/serializers.py
from rest_framework.serializers import ModelSerializer

from .models import Gamebook


class GamebookSerializer(ModelSerializer):
    class Meta:
        model = Gamebook
        fields = ['code', 'title']
        read_only_fields = 'code'
