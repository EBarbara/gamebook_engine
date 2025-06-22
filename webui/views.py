from django.shortcuts import render, get_object_or_404

from gamebooks.models import Gamebook, Paragraph
from gamebooks.utils import build_paragraph_graph, graph_to_dot


def gamebook_list(request):
    books = Gamebook.objects.all()
    return render(request, 'webui/gamebook_list.html', {'books': books})

def read_paragraph(request, code, number):
    book = get_object_or_404(Gamebook, code=code)
    paragraph = get_object_or_404(Paragraph, gamebook=book, number=number)
    return render(request, 'webui/read_paragraph.html', {'book': book, 'paragraph': paragraph})

def gamebook_graph_view(request, code):
    book = get_object_or_404(Gamebook, code=code)
    graph = build_paragraph_graph(book)
    dot_data = graph_to_dot(graph)
    return render(request, 'webui/gamebook_graph.html', {'book': book, 'graph': graph, 'dot': dot_data})
