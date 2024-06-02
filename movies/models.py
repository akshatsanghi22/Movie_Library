
from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    imdb_id = models.CharField(max_length=100, unique=True)
    poster = models.URLField(max_length=200, null=True, blank=True)
    runtime = models.CharField(max_length=50, blank=True)
    ratings = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    box_office = models.CharField(max_length=255, blank=True)
    actors = models.TextField(blank=True)

    def __str__(self):
        return self.title

class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name




