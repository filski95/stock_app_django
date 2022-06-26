from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from stocks_app.models import Stock


class CustomUser(AbstractUser):
    age = models.fields.PositiveSmallIntegerField(validators=[MinValueValidator(15), MaxValueValidator(110)])
    background = models.CharField(max_length=20)  # economics, IT, cs, etc
    stock = models.ManyToManyField(Stock, blank=True)

    # available fields to creasuperuser
    REQUIRED_FIELDS = ["age", "email"]

    def __str__(self) -> str:
        return self.username
