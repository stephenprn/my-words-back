from rest_framework.viewsets import ModelViewSet
from common.views.deletable import DeletableModelViewSetMixin
from words.models.collection import Collection
from words.serializers.collection import CollectionSerializer
from rest_framework.response import Response

from rest_framework.decorators import action
from django.db.models import Q
from rest_framework import status

from words.serializers.collection_indexes import CollectionIndexesSerializer


class CollectionViewSet(DeletableModelViewSetMixin[Collection], ModelViewSet):
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "indexes":
            return CollectionIndexesSerializer

        return CollectionSerializer

    def get_queryset(self):
        queryset = Collection.objects.filter(
            user__id=self.request.user.id, deleted=False
        )

        queryset = queryset.order_by("index")
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response(self.get_queryset().count())

    @action(methods=["post"], detail=False)
    def indexes(self, request):
        SerializerClass = self.get_serializer_class()

        serializer = SerializerClass(data=request.data)
        serializer.is_valid(raise_exception=True)

        langs_indexes_map = {
            lang_index["collection_lang"]: lang_index["index"]
            for lang_index in serializer.data["collection_indexes"]
        }

        collections = self.get_queryset()
        collections = collections.filter(lang__in=list(langs_indexes_map.keys()))

        for collection in collections:
            collection.index = langs_indexes_map[collection.lang]

        Collection.objects.bulk_update(collections, ["index"])

        return Response(status=status.HTTP_202_ACCEPTED)
