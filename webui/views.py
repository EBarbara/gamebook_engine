from django.shortcuts import render, get_object_or_404, redirect

from gamebooks.models import Gamebook, Paragraph, ReadingSession
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

def start_reading_session(request, code):
    book = get_object_or_404(Gamebook, code=code)
    first_paragraph = book.paragraphs.order_by('number').first()

    session = ReadingSession.objects.create(
        book=book,
        current_paragraph=first_paragraph,
        state={}
    )

    return redirect('webui-read-session', session_id=session.id)

def read_session(request, session_id):
    session = get_object_or_404(ReadingSession, id=session_id)
    paragraph = session.current_paragraph

    return render(request, 'webui/read_session.html', {
        'session': session,
        'paragraph': paragraph,
    })

def session_goto_paragraph(request, session_id, target_paragraph_number):
    session = get_object_or_404(ReadingSession, id=session_id)
    target = get_object_or_404(Paragraph, book=session.book, number=target_paragraph_number)
    session.current_paragraph = target
    session.save()
    return redirect('webui-read-session', session_id=session.id)