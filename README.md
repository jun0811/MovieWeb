# README

![](https://img.shields.io/badge/vue-2.0-red)![](https://img.shields.io/badge/django-3.1-green)

# 0. 프로젝트

### 목표.

1. 영화 정보 수집
2. 데이터 베이스 구축 
3. Django 만으로 프로젝트 완성
4. 영화 추천 알고리즘



```bash
localhost:8000/movies/tmdbdata/ 를 통해 db데이터를 입력할 수 있습니다.
```

## 데이터 수집 및 가공 

### 1. 데이터 수집 API

- TMDB(https://www.themoviedb.org/documentation/api)

- top_rated 기준으로 영화정보를 제공받아 django seed data로 활용

  ```python
      g= {
          28 : '액션',
          12 : '모험',
  				.....
          10752 : '전쟁',
          37 : '서부',
          36 : '역사',
      } # 영화 장르 코드 
  
      for genre_name in g.values():
          gerne_instance = Genre()
          gerne_instance.name = genre_name
          gerne_instance.save()
  		.....
   
      for i in range(1,11): # page 1~10 => 총 10개 페이지 
          params = {
              'api_key' :"645b9138c68a71f1de281e4ae381a8b4",
              'language' : 'ko-KR',
              'page' : i,
              'region' : 'KR',
          }
          res = requests.get(BASE_API,params=params).json()
          results = res['results']
          for j in range(20): 
              movie_instance = Movies() # Movies 인스턴스 
  					......
              movie_instance.poster_path = poster_path
              movie_instance.save()
              for gerne in genres: 
                  gerne_instance = Genre.objects.get(name=gerne)
                  movie_instance.genres.add(gerne_instance)
          # for k in range(len(model)):
  ```

  **<문제점>**

  - ManyToMany 관계를 정확히 이해하지 못한 결과, django에서 어떻게 만들어주어야하는지 오래동안 헤맸다.
    - `user.genres.all()`: 유저가 좋아요한 영화 장르들 → 역참조 - M:N   
    - 이러한 관계를 통해 유저가 좋아요한 영화 장르들을 저장하고 역참조를 통해 추천 알고리즘을 만들었다.
  
  
  
  # 2. 데이터베이스 모델링(ERD)
  
  ![final_pjt_ERD](README.assets/final_pjt_ERD.jpg)

- ERD 첫 구상과 달리 많은 구조 변화가 있었다. 처음부터 어떻게 관계를 잘지어야 나중에 웹에서 데이터를 다룰 때  편하다는 것을 제대로 느낄 수 있었다. 

- many-to-many 관계의 유용성은 정말 좋았다. 중계 테이블을 만드는 것이 처음에 어려웠지만 한 번해보니 좀 더 데이터 베이스 관계를 이해할 수 있었다.

  

  # 화면 설계(UI)

  - 카카오 오븐을 통해 설계 

  ![](README.assets/1.PNG)

   **[첫 구상도]**

  ![](README.assets/2.PNG)

  **[실제 구현]**

  위와 같이 실제 예상과는 달랐지만 UI요소가 실제로 해보면서 계속 고치게 되는 것 같다. 전체적인 느낌만 구성하고 지속적인 수정을 통해 완성도를 높여가는 방식으로 프로젝트를 했다. 

  다음 웹 프로젝트는 좀더 UI와 효과에 신경을 두고 싶다.

  ---

  

  ## 3. 기능 

  ### 1.영화 상세페이지
  
  ![](README.assets/3.PNG)
  
  - 주요 기능으로는 `❤좋아요` 버튼을 통해 추천 알고리즘 데이터를 모으는 것과 Youtube API를 통해 예고편을 제공 하였다. 
  
    ```python
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
    ```

  

  ### 2. 영화 검색 기능

  1. 장르별 검색 

     ![](README.assets/4.PNG)

  2. 영화 제목 검색 
  
     ![](README.assets/5.PNG)
  
  ### 3. 커뮤니티 기능
  
  ![](README.assets/1-1606669942702.PNG)

![](README.assets/2-1606669950404.PNG)

- Modal 기능을 사용하여 검색기능을 통한 글 작성

```python
# @require_POST
def search_title(request, title):
    print(title)
    movies = Movies.objects.filter(title__contains=title)
    # print(movies.object.all())
    data = {
        "movies" :movies
    }
    return JsonResponse(list(movies.values()),safe=False)

```

- 또한 댓글 작성 및 글 삭제 수정 기능을 더했다. 
- 아쉬운점⚡ : 댓글 수정기능이 생각보다 쉽지 않았다. Javascript를 활용하여 페이지 리로드 없이 할려고 했지만 잘되지 않아 기능을 뺴고 프로젝트를 수행했다. 추후 댓글 수정 기능을 넣을 것이다.



---

## 4. 배포 

aws를 이용해 배포를 완료하였다. 힘든 과정이었지만 배포를 하고나니 다른사람에게도 사이트를 보여줄 수 있고, 배포 과정을 이해하는데 도움이 되었다.

배포 주소: http://3.35.166.99/movies/



---

## 느낀점 🚗

- javascript와 css를 더 공부해서 멋진 web을 만들고 싶다는 욕심이 생겼다.🌊

- 프론트엔드는 한 사람이 맡는 것이 좋은 것 같다.

  - 우리는 프론트엔드/백엔드 구분 없이 두명 다 같이 했는데, 이렇게 하니 사이트 디자인의 통일성이 부족했다. 내가 맡은 홈페이지와 회원 정보 관리, 회원정보 수정 및 비밀번호 변경 페이지는 검은색과 흰색을 이용한 디자인을 추구했는데, 페어가 맡은 커뮤니티는 민트색과 회색을 이용한 디자인을 추구하였다.
  - 프론트엔드를 한 사람이 다 하거나, 아니면 처음에 UI 설계를 페이지별로 세세하게 같이 구성해놓고 그거대로 페이지를 구현하는 방법이 좋은 것 같다.

- 스타일링은 굉장히 어렵고 시간이 많이 든다.

  - 처음엔 애니메이션도 잔뜩 넣고 깔끔하고 예쁘게 꾸미고 싶었는데, 시간 부족으로 실현하지 못했다.. 그래도 최대한 깔끔하게 스타일링 하려고 노력했는데, css로 스타일링 하는 것은 쉽지 않았다.
  - 스타일링을 예쁘게 하려면 다른 사이트들을 많이 참고해보는 것이 좋은 것 같다. 다음엔 템플릿도 사용해보고, 애니메이션 기능도 구현해보아야겠다.
  - 기능이 아무리 많은 사이트여도 UI가 부족하면 별로여 보인다는 걸 깨달았다. 스타일링은 매우 중요하다!!

  

  ### 아쉬운점 

  - 반응형 디자인을 구현하지 못함

  - 스타일링을 신경쓰지 못함