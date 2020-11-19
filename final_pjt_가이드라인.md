



## 1. 요구사항 분석 및 목표 기능 선정

- 프로젝트 명세서 꼼꼼히 분석
- 주제에 맞는 추가 기능 선정



## 2. 데이터베이스 모델링 (ERD)

- 프로젝트 초기에는 자주 변경될 수 있으므로 자신있게 할 것



## 3. 데이터 수집 및 가공

- 데이터 수집 방법 논의 (API or 크롤링..)
- 충분한 데이터 수집
- 기능 구현에 필요한 형태로 가공



## 4. 화면 설계(UI)

- 핸드 드로잉 or Mockup Tools(카카오 오븐, Adobe XD..)



## 5. 개발



## 6. 테스팅

- 모든 기능이 에러 없이 동작하는 지 확인
- 테스트 코드까진 아니더라도, 직접 **유저의 입장**으로 테스트
- 여유가 되면 예측 가능한 예외까지 처리해둘 것



## 7. 배포 (선택적)

- "Real Artists Ship"



## 8. 문서화

- 프로젝트 소개 README 작성
- SHOW OFF!

```
title = models.CharField(max_length=100)
release_date = models.CharField(max_length=20)
popularity = models.FloatField()
vote_count = models.IntegerField()
vote_average = models.FloatField()
overview = models.TextField()
poster_path = models.CharField(max_length=200)
genres = models.ManyToManyField(Genre)
like_movies = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

```

