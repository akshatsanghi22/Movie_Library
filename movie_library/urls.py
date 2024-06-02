"""
URL configuration for movie_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from movies.views import signup_view, login_view, logout_view,home_view,search,create_movie_list, update_movie_list, delete_movie_list, add_movie_to_list
from movies import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
     path('home/', home_view, name='home'),
    path('search/', views.search, name='search'),
    path('create_list/', create_movie_list, name='create_movie_list'),
    path('update/<int:list_id>/', views.update_movie_list, name='update_movie_list'),
    path('delete_movie_list/<int:list_id>/', views.delete_movie_list, name='delete_movie_list'),
    path('remove_movie_from_list/<int:list_id>/<int:movie_id>/', views.remove_movie_from_list, name='remove_movie_from_list'),
    path('add_movie/', views.add_movie_to_list, name='add_movie_to_list'),
    path('', home_view, name='home'),  # Default to home view
    path('', login_view, name='home'),  # Home view for logged-in users
]

