from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CompanyViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('company', CompanyViewSet)

# viewset routes
urlpatterns = router.urls

# authentication and jwt routes
urlpatterns += [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls'))
]