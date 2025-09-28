from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.name} {self.model}"
