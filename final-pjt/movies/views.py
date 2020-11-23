import requests
from django.views.decorators.http import require_http_methods, require_POST

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Movies, Genre
# Create your views here.
def tmdbdata(request):
    BASE_API = 'https://api.themoviedb.org/3/movie/top_rated'
    g= {
        28 : '액션',
        12 : '모험',
        14 : '판타지',
        878 : '공상과학',
        16 : '애니메이션',
        10402 : '음악',
        10770 : 'TV',
        99 : '다큐',
        18 : '드라마',
        10751 : '가족',
        35 : '코미디',
        10749 : '로맨스',
        53 : '스릴러',
        27 : '공포',
        9648 : '미스터리',
        80 : '범죄',
        10752 : '전쟁',
        37 : '서부',
        36 : '역사',
    }

    for genre_name in g.values(): # Genre 인스턴스 만들기 
        gerne_instance = Genre()
        gerne_instance.name = genre_name
        gerne_instance.save()
        

    url = "https://image.tmdb.org/t/p/w500"
    # models
    for i in range(1,11):
        params = {
            'api_key' :"645b9138c68a71f1de281e4ae381a8b4",
            'language' : 'ko-KR',
            'page' : i,
            'region' : 'KR',
        }
        
        res = requests.get(BASE_API,params=params).json()
        results = res['results']
        for j in range(20):
            movie_instance = Movies() # 나중에 저장 
            genres = []
            genres = [g[id] for id in results[j]["genre_ids"]]
            poster_path = url + results[j]["poster_path"]       
            movie_instance.title = results[j]["title"]
            movie_instance.release_date = results[j]["release_date"]
            movie_instance.popularity = results[j]["popularity"]
            movie_instance.vote_count = results[j]["vote_count"]
            movie_instance.vote_average = results[j]["vote_average"]
            movie_instance.overview = results[j]["overview"]
            movie_instance.movie_id = results[j]["id"]
            movie_instance.poster_path = poster_path
            movie_instance.save()
            
            # 중계 테이블
            for gerne in genres:
                gerne_instance = Genre.objects.get(name=gerne)
                movie_instance.genres.add(gerne_instance)
        # for k in range(len(model)):


def index(request):
    movies = Movies.objects.order_by("?")[0:9]
    # print(movies)
    first = movies[0:3]
    second = movies[3:6]
    third = movies[6:9]
    context = {
        'first': first,
        'second': second,
        'third': third,
    }
    return render(request, 'movies/index.html', context)

@require_POST
def like(request,pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movies, pk=pk)
        user = request.user
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            is_like=False
        else:
            movie.like_users.add(user)
            is_like=True
        data = {
            'is_like' : is_like,
            'like_count' : movie.like_users.count()
        }
        return JsonResponse(data)
    return redirect('accounts:login')


def detail(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)