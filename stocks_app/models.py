from django.db import models
from django.urls import reverse


class Stock(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("stock_detail", kwargs={"pk": self.pk})
