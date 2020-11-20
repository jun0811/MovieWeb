from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from django.views.decorators.http import require_POST, require_http_methods

from .forms import CustomUserCrationForm, CustomUserChangeForm

# Create your views here.
require_http_methods(['GET', 'POST'])
def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('')
    if request.method == 'POST':
        form = CustomUserCrationForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # auth
            form.save()
            return redirect('accounts:signup')  # 수정 필요
    else:
        form = CustomUserCrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    # if request.user.is_authenticated:
    #     return redirect('')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:login') # or 'movies:index'로 수정 필요
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


# @require_POST
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:update')  # 수정 필요
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('accounts:signup') # 수정 필요


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:update') # 수정 필요
    else: 
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
