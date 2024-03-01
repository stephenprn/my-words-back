from rest_framework.viewsets import ModelViewSet
from common.views.deletable import DeletableModelViewSetMixin
from words.models.word_tag import WordTag
from words.serializers.word_tag import WordTagSerializer
from rest_framework.response import Response

from rest_framework.decorators import action
from django.db.models import Q


class WordTagViewSet(DeletableModelViewSetMixin[WordTag], ModelViewSet):
    serializer_class = WordTagSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = WordTag.objects.filter(user__id=self.request.user.id, deleted=False)

        queryset = queryset.order_by("slug")
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response(self.get_queryset().count())
