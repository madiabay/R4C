import uuid
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Robot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    model = models.CharField(
        max_length=2,
        validators=[MinLengthValidator(2), MaxLengthValidator(2)],
        db_index=True
    )
    version = models.CharField(
        max_length=2,
        validators=[MinLengthValidator(2), MaxLengthValidator(2)]
    )
    created = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['model', 'version']),
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f"{self.model}-{self.version}"
