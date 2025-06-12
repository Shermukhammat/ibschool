from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import FAQ, SiteSettings, Post
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def login_required_dec(func):
    return login_required(func, login_url='login')


def main_page(request):
    return render(request, 'main_page.html')


def login_page(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/')  # Change to your success URL
    
    if request.POST:
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Handle remember me functionality
            remember_me = request.POST.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            
            messages.success(request, 'Muvaffaqiyatli kirdingiz!')
            
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, 'Kirish ma\'lumotlarini tekshiring.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Tizimdan muvaffaqiyatli chiqdingiz.')
    return redirect('/login')


def help(request):
    faqs = FAQ.objects.order_by('-created_at').all()
    obj = SiteSettings.get_solo()
    return render(request, 'help.html', {'faqs': faqs, 'settings': obj})


def post(request, year, month, day, slug):
    post = Post.objects.get(
        published__year=year,
        published__month=month,
        published__day=day,
        slug=slug
    )
    if post:
        return render(request, 'post.html', {'post': post})
    return HttpResponse('Maqola topilmadi')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostListView(ListView):
    queryset = Post.published_posts.all()
    context_object_name = 'posts'
    template_name = 'posts.html'
    paginate_by = 6
