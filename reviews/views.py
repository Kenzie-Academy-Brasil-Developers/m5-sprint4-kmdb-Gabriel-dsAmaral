from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Review

from .serializers import ReviewSerializer
from users.models import User
from movies.models import Movie
from django.shortcuts import get_object_or_404
from django.http import Http404
from .permissions import ReviewsPermission
from rest_framework.pagination import PageNumberPagination


class ReviewsView(APIView, PageNumberPagination):
    permission_classes = [ReviewsPermission]

    def post(self, request: Request, movie_id: int):
        token = AccessToken(request.META.get(
            "HTTP_AUTHORIZATION").split(" ")[1])

        if request.data["stars"] > 10:
            return Response(
                {"stars": ["Ensure this value is less than or equal to 10."]},
                status.HTTP_400_BAD_REQUEST,
            )

        if request.data["stars"] < 1:
            return Response(
                {"stars": ["Ensure this value is greater than or equal to 1."]},
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = get_object_or_404(User, pk=token["user_id"])
        except Http404:
            return Response({"message": "User not found."}, status.HTTP_404_NOT_FOUND)

        try:
            movie = get_object_or_404(Movie, pk=movie_id)
        except Http404:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)

        request.data["movie_id"] = movie.id
        request.data["user_id"] = user.id

        serialized = ReviewSerializer(data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id: int):
        reviews = Review.objects.all().filter(movie_id=movie_id)

        result_page = self.paginate_queryset(
            reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class ReviewDeleteView(APIView):
    def delete(self, request: Request, review_id: int):

        token = AccessToken(request.META.get(
            "HTTP_AUTHORIZATION").split(" ")[1])
        user = get_object_or_404(User, pk=token["user_id"])

        try:
            review = get_object_or_404(Review, pk=review_id)
        except Http404:
            return Response({"message": "Review not found."}, status.HTTP_404_NOT_FOUND)

        if (user.is_staff == False and user.is_superuser == False) or (review.user.id != user.id):
            return Response({
                "message": "You are not authorized to do this."
            }, status.HTTP_401_UNAUTHORIZED)

        review.delete()
        return Response("", status.HTTP_204_NO_CONTENT)


class ReviewGetAllView(APIView, PageNumberPagination):
    permission_classes = [ReviewsPermission]

    def get(self, request: Request):
        reviews = Review.objects.all()

        result_page = self.paginate_queryset(
            reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
