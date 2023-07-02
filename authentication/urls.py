from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CompanyViewSet, GithubOAuth2, GoogleOAuth2, LinkedinOAuth2,
                    UserViewSet)

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('company', CompanyViewSet)

# viewset routes
urlpatterns = router.urls

# authentication and jwt routes
urlpatterns += [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls')),
    path('', include('social_django.urls')),
    path('oauth2/google/', GoogleOAuth2.as_view()),
    path('oauth2/linkedin/', LinkedinOAuth2.as_view()),
    path('oauth2/github/', GithubOAuth2.as_view()),
]
