from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=60)
    last_name = serializers.CharField(max_length=60)
    password = serializers.CharField(max_length=128, write_only=True)

    date_joined = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_email(self, email: str):
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValueError({"detail": ["email already exists."]}, 409)

        return email

    def validate_password(self, password: str):
        password = make_password(password)
        return password

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class UserCriticSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    first_name = serializers.CharField(max_length=60)
    last_name = serializers.CharField(max_length=60)
