from django.urls import path
from .views import MesureListAPIView

urlpatterns = [
    path(
        'mesures/',
        MesureListAPIView.as_view(),
        name='mesures-list'
    ),
]