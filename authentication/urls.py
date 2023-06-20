from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register('profile', ProfileViewSet)

# viewset routes
urlpatterns = router.urls

# authentication and jwt routes
urlpatterns += [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]