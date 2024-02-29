from django.db import models
from common.models.deletable import DeletableModelMixin
from common.models.timestamped import TimestampedModelMixin
from django.conf import settings
from django.core.validators import MinValueValidator

from common.models.uuid import UuidModelMixin


class Collection(TimestampedModelMixin, UuidModelMixin, DeletableModelMixin):
    lang = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="collections", on_delete=models.CASCADE)
    index = models.IntegerField(validators=[MinValueValidator(1)])
