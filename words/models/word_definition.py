from django.db import models
from common.models.timestamped import TimestampedModelMixin

from common.models.uuid import UuidModelMixin

class WordDefinition(TimestampedModelMixin, UuidModelMixin):
    word = models.CharField(max_length=255)
    definition = models.TextField()
    note = models.TextField()
    slug = models.CharField(max_length=255)
