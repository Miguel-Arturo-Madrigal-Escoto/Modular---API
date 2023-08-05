from rest_framework.routers import DefaultRouter

from .views import FormViewSet

router = DefaultRouter()

router.register('data', FormViewSet, basename='form-data')

urlpatterns = router.urls
