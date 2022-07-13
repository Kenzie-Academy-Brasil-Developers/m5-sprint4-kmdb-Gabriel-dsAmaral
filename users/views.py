from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from .permissions import UsersPermission
from users.models import User
from users.serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserPostView(APIView):
    def post(self, request: Request):
        serialized = UserSerializer(data=request.data)
        try:
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_201_CREATED)

        except ValueError as err:
            return Response(*err.args)


class UserGetView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [UsersPermission]

    def get(self, request: Request):
        users = User.objects.all()
        result_page = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserGetByIdView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [UsersPermission]

    def get(self, _: Request, user_id: int):
        try:
            user = get_object_or_404(User, pk=user_id)

            serialized = UserSerializer(user)
            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "User not found."}, status.HTTP_404_NOT_FOUND)
