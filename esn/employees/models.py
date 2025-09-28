from django.contrib.auth import get_user_model
from django.db import models

from network.models import NetworkNode

User = get_user_model()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    def __str__(self):
        return f"Employee ID {self.pk}"
