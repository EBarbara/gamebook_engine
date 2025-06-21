# gamebooks/serializers.py
from rest_framework.serializers import ModelSerializer

from .models import Gamebook, Paragraph, Choice


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'target']


class ParagraphSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Paragraph
        fields = ['number', 'text', 'combat_enemy', 'combat_skill', 'combat_stamina', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        paragraph = Paragraph.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(paragraph=paragraph, **choice_data)
        return paragraph

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', [])
        # Atualizar os campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualizar choices: simplificando, vamos deletar e recriar
        instance.choices.all().delete()
        for choice_data in choices_data:
            Choice.objects.create(paragraph=instance, **choice_data)

        return instance

class GamebookDetailsSerializer(ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Gamebook
        fields = ['code', 'title', 'paragraphs']

class GamebookListSerializer(ModelSerializer):
    class Meta:
        model = Gamebook
        fields = ['code', 'title']
