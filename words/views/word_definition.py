from rest_framework.viewsets import ModelViewSet
from common.views.deletable import DeletableModelViewSetMixin
from words.models.word_definition import WordDefinition
from words.models.word_tag import WordTag
from words.serializers.word_definition import (
    WordDefinitionDetailSerializer,
    WordDefinitionInputSerializer,
)
from rest_framework.response import Response

from rest_framework.decorators import action
from django.db.models import Q, Prefetch


class WordDefinitionViewSet(DeletableModelViewSetMixin[WordDefinition], ModelViewSet):
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return WordDefinitionInputSerializer

        return WordDefinitionDetailSerializer

    def get_queryset(self):
        queryset = WordDefinition.objects.filter(
            user__id=self.request.user.id, deleted=False
        ).prefetch_related(Prefetch('tags', queryset=WordTag.objects.order_by('slug')), 'collection')

        q = self.request.query_params.get("q")
        collection_in = self.request.query_params.get("collectionIn")
        tag_in = self.request.query_params.get("tagIn")

        if q:
            queryset = queryset.filter(
                Q(word__unaccent__icontains=q)
                | Q(definition__unaccent__icontains=q)
            )

        if collection_in:
            queryset = queryset.filter(
                collection__lang__in=collection_in.split(",")
            )

        if tag_in:
            queryset = queryset.filter(
                tags__slug__in=tag_in.split(",")
            )

        queryset = queryset.order_by("slug")
        return queryset.distinct()

    def get_serializer_context(self):
        return {"request": self.request}

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response(self.get_queryset().count())
