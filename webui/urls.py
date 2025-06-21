from django.urls import path

from .views import gamebook_list

urlpatterns = [
    path('gamebooks/', gamebook_list, name='gamebook-list'),
]