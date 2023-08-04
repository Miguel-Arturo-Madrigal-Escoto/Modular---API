from rest_framework.routers import DefaultRouter

from .views import CompanyRolesViewSet, RolesViewSet

router = DefaultRouter()
router.register('company-roles', CompanyRolesViewSet)
router.register('roles', RolesViewSet)

urlpatterns = router.urls
