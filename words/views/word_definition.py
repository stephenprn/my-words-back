from rest_framework.viewsets import ModelViewSet
from common.views.deletable import DeletableModelViewSetMixin
from words.models.word_definition import WordDefinition
from words.serializers.word_definition import WordDefinitionSerializer
from rest_framework.response import Response

from rest_framework.decorators import action


class WordDefinitionViewSet(ModelViewSet, DeletableModelViewSetMixin[WordDefinition]):
    serializer_class = WordDefinitionSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = WordDefinition.objects.filter(
            user__id=self.request.user.id, deleted=False
        )

        if self.request.query_params.get('q'):
            queryset = queryset.filter(
                word__unaccent__icontains=self.request.query_params.get('q')
            )

        queryset = queryset.order_by("slug")
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response(self.get_queryset().count())
