from rest_framework.routers import DefaultRouter

from .views import CompanyRolesViewSet

router = DefaultRouter()
router.register('roles', CompanyRolesViewSet)

urlpatterns = router.urls
