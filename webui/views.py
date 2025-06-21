from django.shortcuts import render

from gamebooks.models import Gamebook


def gamebook_list(request):
    books = Gamebook.objects.all()
    return render(request, 'webui/gamebook_list.html', {'books': books})