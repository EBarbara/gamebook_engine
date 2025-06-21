from django.shortcuts import render, get_object_or_404

from gamebooks.models import Gamebook, Paragraph


def gamebook_list(request):
    books = Gamebook.objects.all()
    return render(request, 'webui/gamebook_list.html', {'books': books})

def read_paragraph(request, code, number):
    book = get_object_or_404(Gamebook, code=code)
    paragraph = get_object_or_404(Paragraph, gamebook=book, number=number)
    return render(request, 'webui/read_paragraph.html', {'book': book, 'paragraph': paragraph})