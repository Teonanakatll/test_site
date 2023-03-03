from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import archive, about, contact, WomenHome, WomenCategory, ShowPost, AddPage, RegisterUser, LoginUser, \
    logout_user

urlpatterns = [
    path('', cache_page(60)(WomenHome.as_view()), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', cache_page(60)(WomenCategory.as_view()), name='category'),

    # path('cats/<int:catid>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]