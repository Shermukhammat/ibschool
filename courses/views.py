from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Course
# Create your views here.


@login_required(login_url='/login')
def main_page(request):
    return render(request, 'courses.html') 


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CourseListView(ListView):
    def get_queryset(self):
        return Course.objects.filter(groups=self.request.user.group)
    context_object_name = 'courses'
    template_name = 'courses.html'
    paginate_by = 6