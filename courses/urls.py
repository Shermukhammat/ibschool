from . import views
from django.urls import path, re_path

urlpatterns = [
    path('<slug:slug>', views.course_page, name='course'),
    path('<slug:coures_slug>/<slug:modul_slug>/<slug:lesson_slug>', views.lesson_page, name='course'),
    path('', views.CourseListView.as_view(), name='courses')
]