from django.urls import path
from rest_framework_simplejwt import views
from users.views import UserPostView, UserGetView, UserGetByIdView

urlpatterns = [
    path("users/register/", UserPostView.as_view()),
    path("users/", UserGetView.as_view()),
    path("users/<int:user_id>/", UserGetByIdView.as_view()),
    path("users/login/", views.TokenObtainPairView.as_view()),
    path("users/login/refresh/", views.TokenRefreshView.as_view()),
]
