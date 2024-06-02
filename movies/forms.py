# movies/forms.py
from .models import MovieList

from django import forms

class MovieSearchForm(forms.Form):
    query = forms.CharField(label='Search for a movie', max_length=100)
class MovieListForm(forms.ModelForm):
    class Meta:
        model = MovieList
        fields = ['name', 'movies']

class AddMovieForm(forms.Form):
    imdb_id = forms.CharField(label='IMDB ID')
    list_name = forms.CharField(label='List Name', required=False)
