from rest_framework.routers import DefaultRouter

from .views import MatchViewSet

router = DefaultRouter()

router.register('match', MatchViewSet)

urlpatterns = router.urls
