from rest_framework import serializers, status
from .models import Movie
from genres.serializers import GenreSerializer
from genres.models import Genre


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres:
            genre, _ = Genre.objects.get_or_create(**genre)
            movie.genres.add(genre)

        return movie

    def update(self, instance: Movie, validated_data: dict):
        non_updatable = {"genres"}

        for key, value in validated_data.items():
            if key in non_updatable:
                raise KeyError(
                    {"message": f"You can not update the {key} property."},
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            setattr(instance, key, value)
            instance.save()

        return instance
