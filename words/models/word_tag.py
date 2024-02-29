from django.db import models
from common.models.deletable import DeletableModelMixin
from common.models.timestamped import TimestampedModelMixin
from django.conf import settings
from django.core.validators import MinValueValidator

from common.models.uuid import UuidModelMixin
from words.models.word_definition import WordDefinition


class WordTag(TimestampedModelMixin, UuidModelMixin, DeletableModelMixin):
    label = models.CharField(max_length=255)
    emoji = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tags", on_delete=models.CASCADE)
    words = models.ManyToManyField(WordDefinition, related_name="tags")