from django.urls import path, re_path

from .views import index, categories, archive, about

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('cats/<int:catid>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]