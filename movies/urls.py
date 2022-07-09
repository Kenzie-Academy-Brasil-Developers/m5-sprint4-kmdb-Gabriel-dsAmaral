from django.urls import path

from movies.views import MoviesIdView, MoviesView

urlpatterns = [
    path("movies/", MoviesView.as_view()),
    path("movies/<int:movie_id>/", MoviesIdView.as_view()),
]
