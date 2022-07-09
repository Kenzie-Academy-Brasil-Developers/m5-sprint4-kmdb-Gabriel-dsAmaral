from django.db import models


class ReviewRecomendation(models.TextChoices):
    MUST = ("Must Watch", "Must Watch")
    SHOULD = ("Should Watch", "Should Watch")
    AVOID = ("Avoid Watch", "Avoid Watch")
    NO = ("No Opinion", "No Opinion")


class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=50,
        choices=ReviewRecomendation.choices,
        default=ReviewRecomendation.NO,
    )

    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    movie = models.ForeignKey(to="movies.Movie", on_delete=models.CASCADE)
