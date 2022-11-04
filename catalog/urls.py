from rest_framework.routers import SimpleRouter

from catalog.views import BookViewSet, UserBookRelationViewSet

router = SimpleRouter()
router.register('', BookViewSet, 'catalog')
router.register('book_action', UserBookRelationViewSet, 'book')

urlpatterns = router.urls
