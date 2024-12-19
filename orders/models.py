import uuid
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

from customers.models import Customer


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        validators=[MinLengthValidator(5), MaxLengthValidator(5)],
    )
