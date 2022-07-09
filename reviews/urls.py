from django.urls import path

from .views import ReviewsView, ReviewDeleteView, ReviewGetAllView

urlpatterns = [
    path("movies/<int:movie_id>/reviews/", ReviewsView.as_view()),
    path("reviews/<int:review_id>/", ReviewDeleteView.as_view()),
    path("reviews/", ReviewGetAllView.as_view()),
]
