from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from . import views



urlpatterns = [
    re_path('^login/?$', views.login_page, name='login_page'),
    re_path('^logout/?$', views.logout_view, name='logout_page'),
    re_path('^help/?$', views.help, name='help_page'),
    re_path('^posts/?$', views.PostListView.as_view(), name='posts_page'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post, name='post'),
    path('', views.main_page, name='main_page'),
]