from django.db import models
from common.models.deletable import DeletableModelMixin
from common.models.timestamped import TimestampedModelMixin
from django.conf import settings

from common.models.uuid import UuidModelMixin


class WordDefinition(TimestampedModelMixin, UuidModelMixin, DeletableModelMixin):
    word = models.CharField(max_length=255)
    definition = models.TextField()
    note = models.TextField(null=True, blank=True)
    example = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "slug"], name="user_slug_unique")
        ]
