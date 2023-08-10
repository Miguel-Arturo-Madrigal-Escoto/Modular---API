from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CompanyRolesViewSet, RolesAPIView

router = DefaultRouter()
router.register('company-roles', CompanyRolesViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('roles/', RolesAPIView.as_view())
]
