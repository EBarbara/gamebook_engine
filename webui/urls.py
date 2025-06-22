from django.urls import path

from .views import gamebook_list, read_paragraph, gamebook_graph_view

urlpatterns = [
    path('gamebooks/', gamebook_list, name='gamebook-list'),
    path('gamebooks/<str:code>/read/<int:number>', read_paragraph, name='read-paragraph'),
    path('gamebooks/<slug:code>/graph-view/', gamebook_graph_view, name='gamebook-graph-view'),
]