from django.urls import path

from .views import SectorsAPIView

urlpatterns = [
    path('sectors/', SectorsAPIView.as_view())
]
