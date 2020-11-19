from django.shortcuts import render
import requests
from .models import Movies, Genre
# Create your views here.
def tmdbdata(request):
    BASE_API = 'https://api.themoviedb.org/3/movie/top_rated'
    models = ['title','release_date','popularity',
    'vote_count','vote_average','overview','poster_path','genre_ids']
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

    for genre_name in g.values():
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
            # print(genres)
            # print(genres)
            poster_path = url + results[j]["poster_path"]       
            movie_instance.title = results[j]["title"]
            movie_instance.release_date = results[j]["release_date"]
            movie_instance.popularity = results[j]["popularity"]
            movie_instance.vote_count = results[j]["vote_count"]
            movie_instance.vote_average = results[j]["vote_average"]
            movie_instance.overview = results[j]["overview"]
            movie_instance.poster_path = poster_path
            # movie_instance.genres = genres
            movie_instance.save()
            
            # 중계 테이블
            for gerne in genres:
                gerne_instance = Genre.objects.get(name=gerne)
                movie_instance.genres.add(gerne_instance)
        # for k in range(len(model)):

