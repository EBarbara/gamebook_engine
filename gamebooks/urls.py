from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import GamebookViewSet, ParagraphViewSet, gamebook_graph

router = DefaultRouter()
router.register('gamebooks', GamebookViewSet, basename='gamebooks')

paragraphs_router = NestedDefaultRouter(router, 'gamebooks', lookup='gamebook')
paragraphs_router.register('paragraphs', ParagraphViewSet, basename='gamebook-paragraphs')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(paragraphs_router.urls)),
    path('gamebooks/<slug:code>/graph/', gamebook_graph, name='gamebook-graph'),
]