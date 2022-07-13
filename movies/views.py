from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from movies.serializers import MovieSerializer
from movies.models import Movie
from .permissions import MoviesPermission
from rest_framework.pagination import PageNumberPagination


class MoviesView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MoviesPermission]

    def post(self, request: Request):
        serialized = MovieSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)

    def get(self, request: Request):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class MoviesIdView(APIView):
    permission_classes = [MoviesPermission]

    def get(self, _: Request, movie_id: int):
        try:
            movie = get_object_or_404(Movie, pk=movie_id)

            serialized = MovieSerializer(movie)
            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, movie_id: int):
        try:
            movie = get_object_or_404(Movie, pk=movie_id)

            serialized = MovieSerializer(movie, request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)

        except KeyError as err:
            return Response(*err.args)

    def delete(self, _: Request, movie_id: int):
        try:
            movie = get_object_or_404(Movie, pk=movie_id)

            movie.delete()
            return Response("", status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)
