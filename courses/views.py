from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Course, Modul, Lesson
from django.urls import reverse

# Create your views here.


@login_required(login_url='/login')
def course_page(request: HttpRequest, slug: str):
    course = Course.objects.filter(groups = request.user.group, slug = slug).first()
    if course:
        return render(request, 'course.html', {'course': course})
    return render(request, 'nofound.html')
    # return render(request, 'course.html') 


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CourseListView(ListView):
    def get_queryset(self):
        return Course.objects.filter(groups=self.request.user.group).order_by('created_at')
    context_object_name = 'courses'
    template_name = 'courses.html'
    paginate_by = 6



@login_required(login_url='/login')
def lesson_page(request: HttpRequest, coures_slug: str, modul_slug: str, lesson_slug: str):
    lesson = Lesson.objects.filter(slug=lesson_slug,
                            modul__slug=modul_slug,
                            modul__course__slug=coures_slug).first()
    if not lesson:
        return render(request, 'nofound.html')
    
    prev = lesson.get_previous_lesson()
    next = lesson.get_next_lesson()
    back_url = request.GET.get('back')
    return render(request, 'lesson.html', {'lesson': lesson, 'back_url': back_url, 'prev': prev, 'next': next})