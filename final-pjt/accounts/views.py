from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User
from community.models import Review
from django.views.decorators.http import require_POST, require_http_methods
# from ..movies.models import Genre
from .forms import CustomUserCrationForm, CustomUserChangeForm

# Create your views here.
require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustomUserCrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)



@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index') 
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def profile(request, username):
    person = get_object_or_404(User, username=username)
    like_movies = []
    like_genres = []

    genres ={ 
        '액션' : 0,'모험' : 0,'판타지': 0,'공상과학': 0,'애니메이션': 0,
        '음악': 0, 'TV' : 0, '다큐': 0, '드라마':0, '가족': 0,'코미디' : 0,
        '로맨스': 0, '스릴러': 0, '공포': 0, '미스터리': 0, '범죄': 0,
        '전쟁':0,'서부':0,'역사':0

    }
    # 장르 딕셔너리를 미리 만들어서 카운트....한다음에 TOP3개만 담는다.
    
    for movie in person.like_movies.all():
        like_movies.append(movie)
        for genre in movie.genres.all():
            genres[genre.name] +=1
    top_3 = sorted(genres.items(), reverse=True, key= lambda x : x[1])[:3] # 선호도 가장 높은 3개
    # print(top_3)
    for i in range(3):
        if top_3[i][1] != 0:
            like_genres.append(top_3[i][0])
    # print(like_genres)
    context ={
        'person': person,
        'like_movies': like_movies,
        "like_genres" : like_genres,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    print(request.user)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.username) 
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@require_POST
def delete(request):
    print('hi')
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('movies:index')


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user.username)
    else: 
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

