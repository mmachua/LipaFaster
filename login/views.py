
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.forms import RegistrationForm
from login.forms import RegistrationForm , EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import contactForm
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView , CreateView
#from home.models import Post, Friend
#from .models import HitCountMixin, HitCount
#from django.contrib.contenttypes.fields import GenericRelation
#from django.utils.encoding import python_2_unicode_compatible
# Create your views here.


def about(request):
    context = locals()
    #template = 'about.html'
    form = contactForm(request.POST or None)

    if form.is_valid():
        print( request.POST)
        context = locals()

    return render(request, 'login/about.html',context )
 

class SignUpView(CreateView):
    template_name = 'login/reg_form.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'User'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')




#jj
#@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        posts = Post.objects.filter(user=user).order_by("-date")
    else:
        user = request.user
        #user = User.objects.get(pk=pk)
        posts = Post.objects.filter(user=request.user.id).order_by("-date")
    #args = {'user': request.user}
    return render(request,('login/profile.html'), {'user': user, "posts":posts})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect( 'login:view_profile' )

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'login/edit_profile.html', args)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user )

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect( 'login:view_profile' )

        else:
            return redirect('/login/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'login/edit_profile.html', args)
@login_required
def login_admin(request):
    return render(request, 'admin/login.html') 

def logout(request):
    return render(request, 'login/logout.html') 