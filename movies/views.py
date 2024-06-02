from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, MovieList
from .forms import MovieListForm, AddMovieForm
from django.conf import settings
import requests
from .forms import MovieSearchForm


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'movies/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'movies/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    movie_lists = MovieList.objects.filter(user=request.user)
    return render(request, 'movies/home.html', {'movie_lists': movie_lists})

@login_required
def search(request):
    form = MovieSearchForm(request.GET or None)
    movies = []
    if form.is_valid():
        query = form.cleaned_data.get('query')
        api_key = settings.OMDB_API_KEY
        url = f'http://www.omdbapi.com/?apikey={api_key}&s={query}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                movies = data['Search']
    return render(request, 'movies/search.html', {'form': form, 'movies': movies})

@login_required
def create_movie_list(request):
    if request.method == 'POST':
        form = MovieListForm(request.POST)
        if form.is_valid():
            movie_list = form.save(commit=False)
            movie_list.user = request.user
            movie_list.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = MovieListForm()
    return render(request, 'movies/create_movie_list.html', {'form': form})

@login_required
def update_movie_list(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id, user=request.user)
    if request.method == 'POST':
        form = MovieListForm(request.POST, instance=movie_list)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MovieListForm(instance=movie_list)
    return render(request, 'movies/update_movie_list.html', {'form': form})

@login_required
def delete_movie_list(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id, user=request.user)
    if request.method == 'POST':
        movie_list.delete()
        return redirect('home')
    return render(request, 'movies/delete_movie_list.html', {'movie_list': movie_list})

@login_required
def remove_movie_from_list(request, list_id, movie_id):
    movie_list = get_object_or_404(MovieList, id=list_id, user=request.user)
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie_list.movies.remove(movie)
        movie_list.save()
        return redirect('home')

    return render(request, 'movies/home.html', {'movie_list': movie_list})

def add_movie_to_list(request):
    if request.method == 'POST':
        imdb_id = request.POST.get('imdb_id')
        list_name = request.POST.get('list_name')

        if not list_name:
            list_name = 'default'

        movie_list, created = MovieList.objects.get_or_create(name=list_name, user=request.user)

        if imdb_id:
            api_key = settings.OMDB_API_KEY
            url = f'http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    movie, created = Movie.objects.get_or_create(
                        imdb_id=imdb_id,
                        defaults={
                            'title': data.get('Title', ''),
                            'year': data.get('Year', ''),
                            'poster': data.get('Poster', ''),
                            'runtime': data.get('Runtime', ''),
                            'ratings': data.get('imdbRating', ''),
                            'genre': data.get('Genre', ''),
                            'box_office': data.get('BoxOffice', ''),
                            'actors': data.get('Actors', '')
                        }
                    )
                    movie_list.movies.add(movie)
                    movie_list.save()
    return redirect('home')
