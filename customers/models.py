import uuid
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name