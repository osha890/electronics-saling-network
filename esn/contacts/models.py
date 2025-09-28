from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.city}, {self.country}"


class Contact(models.Model):
    email = models.EmailField()
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Contact ID {self.pk}"
