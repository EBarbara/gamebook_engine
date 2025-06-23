from django.urls import path

from .views import (
    gamebook_list, read_paragraph, gamebook_graph_view, start_reading_session, read_session, session_goto_paragraph,
    home
)

urlpatterns = [
    path('', home, name='home'),
    path('gamebooks/', gamebook_list, name='gamebook-list'),
    path('gamebooks/<str:code>/read/<int:number>', read_paragraph, name='read-paragraph'),
    path('gamebooks/<slug:code>/graph-view/', gamebook_graph_view, name='gamebook-graph'),
    path('gamebooks/<slug:code>/start-session/', start_reading_session, name='start-reading-session'),
    path('gamebooks/sessions/<int:session_id>/', read_session, name='read-session'),
    path('gamebooks/sessions/<int:session_id>/goto/<int:target_paragraph_number>/', session_goto_paragraph, name='webui-session-goto'),
]