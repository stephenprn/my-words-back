from rest_framework.viewsets import ModelViewSet
from common.views.deletable import DeletableModelViewSetMixin
from words.models.word_definition import WordDefinition
from words.serializers.word_definition import (
    WordDefinitionDetailSerializer,
    WordDefinitionInputSerializer,
)
from rest_framework.response import Response

from rest_framework.decorators import action
from django.db.models import Q


class WordDefinitionViewSet(DeletableModelViewSetMixin[WordDefinition], ModelViewSet):
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return WordDefinitionInputSerializer

        return WordDefinitionDetailSerializer

    def get_queryset(self):
        queryset = WordDefinition.objects.filter(
            user__id=self.request.user.id, deleted=False
        )

        if self.request.query_params.get("q"):
            queryset = queryset.filter(
                Q(word__unaccent__icontains=self.request.query_params.get("q"))
                | Q(definition__unaccent__icontains=self.request.query_params.get("q"))
            )

        if self.request.query_params.get("collectionIn"):
            queryset = queryset.filter(
                collection__lang__in=self.request.query_params.get(
                    "collectionIn"
                ).split(",")
            )

        queryset = queryset.order_by("slug")
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response(self.get_queryset().count())
