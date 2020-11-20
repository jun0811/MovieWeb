from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCrationForm

# Create your views here.
def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('')
    if request.method == 'POST':
        form = CustomUserCrationForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # auth
            form.save()
            return redirect('accounts:signup')
    else:
        form = CustomUserCrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    # if request.user.is_authenticated:
    #     return redirect('')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:login') # or 'movies:index'
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)