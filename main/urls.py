from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views



urlpatterns = [
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_view, name='logout_page'),
    path('help', views.help, name='help_page'),
    path('posts/', views.PostListView.as_view(), name='posts_page'),
    path('posts', views.PostListView.as_view(), name='posts_page'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post, name='post'),
    path('', views.main_page, name='main_page'),
]