import requests
from django.views.decorators.http import require_http_methods, require_POST
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
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
    # movie Carousel 
    movies = Movies.objects.order_by("?")[0:9]
    first = movies[0:3]
    second = movies[3:6]
    third = movies[6:9]
    # user 정보 
    genres ={ 
        '1' : 0,'2' : 0,'3': 0,'4': 0,'5': 0,
        '6': 0, '7' : 0, '8': 0, '9':0, '10': 0,'11' : 0,
        '12': 0, '13': 0, '14': 0, '15': 0, '16': 0,
        '17':0,'18':0,'19':0
    } #장르 테이블에 맞추어서 딕셔너리 구성 
    like_genres = []
    recommand = []
    if request.user.is_authenticated:
        user = request.user
        # print(Movies.objects.all())
        for movie in user.like_movies.all():
            for genre in movie.genres.all():
                # print(genre.id)
                genres[str(genre.id)] +=1
        top_2 = sorted(genres.items(), reverse=True, key= lambda x : x[1])[:2] # 선호도 가장 높은 3개
        if top_2[0][1] != 0:
            for i in range(2):
                like_genres.append(top_2[i][0])
            for movie in Movies.objects.order_by('-popularity'):
                
                for genre in movie.genres.all():
                    # print(genre.id)  
                    if (str(genre.id) in like_genres) and movie not in recommand:
                        recommand.append(movie)
            recommand = recommand[:3]
    # recommand = list(set(recommand))[:3]

    context = {
        'first': first,
        'second': second,
        'third': third,
        'recommand': recommand
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
    else:
        movie = get_object_or_404(Movies, pk=pk)
        # user = request.user
        is_like = False
        data ={
            'is_like' : is_like,
            'like_count' : movie.like_users.count()
        }
        return JsonResponse(data)


def youtube(title):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key' : settings.YOUTUBE_API_KEY,
        'part' : 'snippet',
        'type' : 'video',
        'maxResults': '1',
        'q' : f'{title} trailer' 
    }
    response = requests.get(url,params)
    response_dict = response.json()
    return response_dict


def detail(request, movie_pk):
    movie = get_object_or_404(Movies, pk=movie_pk)
    genres = movie.genres.all().values()
    trailer = youtube(movie.title)
    context = {
        'movie': movie,
        'genres': genres,
        'trailer': trailer['items'][0]['id']['videoId']
    }
    return render(request, 'movies/detail.html', context)



def search_genre(request, genre):
    movies = Movies.objects.all()
    results = []
    for movie in movies:
        for gen in movie.genres.all():
            # print(type(gen.id))
            if int(genre) == gen.id:
                results.append(movie)
    # print(result)
    context ={
        'results' : results,
    }
    return render(request, 'movies/search_genre.html',context)


# page = 8페이지

def top_ratedlist(request,page):
    # movie_items = 200

    movies = Movies.objects.all()
    movies = movies[0+(24*page):24+(24*page)]
    context = {
        'movies': movies,
    }
    return render(request, 'movies/top_ratedlist.html', context)


def search(request, input):
    movies = Movies.objects.all()
    result = []
    for movie in movies:
        if input in movie.title:
            result.append([movie.poster_path, movie.pk])
    print(result)
    data = {
        'result': result,
    }
    return JsonResponse(data)