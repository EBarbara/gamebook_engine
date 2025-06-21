import random

from django.db.models import Choices
from ninja import NinjaAPI

from .models import Gamebook, Paragraph, Choice

api = NinjaAPI()

@api.get("/gamebooks")
def list_gamebooks(request):
    books = Gamebook.objects.all()
    return list(books)

@api.get("/gamebook/{book_code}/paragraph/{number}")
def get_paragraph(request, book_code:str, number:int):
    try:
        book = Gamebook.objects.get(code=book_code)
        paragraph = Paragraph.objects.get(gamebook=book, number=number)
        choices = list(Choice.objects.filter(paragraph=paragraph))

        return {
            "text": paragraph.text,
            "combat": {
                "enemy": paragraph.combat_enemy,
                "skill": paragraph.combat_skill,
                "stamina": paragraph.combat_stamina,
            } if paragraph.combat_enemy else None,
            "choices": choices,
        }
    except (Gamebook.DoesNotExist, Paragraph.DoesNotExist):
        return {"error": "Parágrafo não encontrado"}


@api.get("/roll_dice")
def roll_dice(request, n: int = 2):
    return {"result": sum(random.randint(1, 6) for _ in range(n))}
