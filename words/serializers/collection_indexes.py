from rest_framework import serializers
from django.core.validators import MinValueValidator


class CollectionIndexSerializer(serializers.Serializer):
    collection_lang = serializers.CharField()
    index = serializers.IntegerField(validators=[MinValueValidator(1)])


class CollectionIndexesSerializer(serializers.Serializer):
    collection_indexes = CollectionIndexSerializer(many=True)

    def validate_collection_indexes(self, collection_indexes):
        if len(collection_indexes) < 1:
            raise serializers.ValidationError("Specify at least one index")

        return collection_indexes
