from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.name
