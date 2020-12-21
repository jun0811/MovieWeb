from django.db import models
# from django_random_queryset import RandomManager
from django.conf import settings

# Create your models here.
class Genre(models.Model):

    name = models.CharField(max_length=50)


class Movies(models.Model):
    title = models.CharField(max_length=100)
    movie_id = models.IntegerField()
    release_date = models.CharField(max_length=20)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name= 'movie_genre')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')