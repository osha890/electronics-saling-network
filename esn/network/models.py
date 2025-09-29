from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from contacts.models import Contact
from network.choices import NetworkNodeType
from products.models import Product


class NetworkNode(models.Model):
    name = models.CharField(max_length=255)

    type = models.CharField(max_length=20, choices=NetworkNodeType.choices)

    contact = models.OneToOneField(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    products = models.ManyToManyField(
        Product,
        blank=True,
    )

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
    )

    debt_to_supplier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.type == NetworkNodeType.FACTORY and self.supplier is not None:
            raise ValidationError("A Factory cannot have a supplier.")
        if self.supplier is None and self.debt_to_supplier != 0:
            raise ValidationError("Debt to supplier must be 0 if there is no supplier.")
        if self.supplier == self:
            raise ValidationError("A node can't be it's own supplier.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
