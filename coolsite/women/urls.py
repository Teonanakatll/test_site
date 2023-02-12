from django.urls import path

from .views import index, categories

urlpatterns = [
    path('', index),
    path('cats/<int:catid>/', categories),
]