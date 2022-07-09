from rest_framework import serializers, status
from .models import Review
from users.serializers import UserCriticSerializer


class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    stars = serializers.IntegerField()
    review = serializers.CharField()
    spoilers = serializers.BooleanField(default=False)
    movie_id = serializers.IntegerField()
    user_id = serializers.IntegerField(write_only=True)
    critic = UserCriticSerializer(source="user")
    recomendation = serializers.ChoiceField(
        allow_null=True,
        choices=(
            ("Must Watch", "Must Watch"),
            ("Should Watch", "Should Watch"),
            ("Avoid Watch", "Avoid Watch"),
            ("No Opinion", "No Opinion"),
        ),
    )

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)

        return review
