from core.models import CoreModel
from django.db import models


class Client(CoreModel):
    name = models.CharField("Name", max_length=100)

    class Meta:
        app_label = "clients"
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
