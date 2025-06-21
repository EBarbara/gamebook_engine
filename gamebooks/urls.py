from rest_framework.routers import DefaultRouter

from .views import GamebookViewSet, ParagraphViewSet

router = DefaultRouter()
router.register('gamebooks', GamebookViewSet)
router.register('paragraphs', ParagraphViewSet)