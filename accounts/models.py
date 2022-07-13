from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from stocks_app.models import Stock


class CustomUser(AbstractUser):
    age = models.fields.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(110)])
    background = models.CharField(max_length=20)  # economics, IT, cs, etc
    stock = models.ManyToManyField(Stock, related_name="user", blank=True)
    # related_name -> added so that: 1. stocks API can reference users who have them on watchlists
    # 2. easier lookups in Watchlist view -> customuser__username=self.request.user replaced user = self.request.user [reverse relationship]

    REQUIRED_FIELDS = ["age", "email"]  # available fields to superuser

    def __str__(self) -> str:
        return self.username
