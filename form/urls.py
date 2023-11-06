from rest_framework.routers import DefaultRouter

from .views import CompanySeedViewSet, FormViewSet, UserSeedViewSet

router = DefaultRouter()

router.register('data', FormViewSet, basename='form-data')
router.register('db-user-seed', UserSeedViewSet, basename='db-user-seed')
router.register('db-company-seed', CompanySeedViewSet, basename='db-company-seed')

urlpatterns = router.urls
