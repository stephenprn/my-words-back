from rest_framework import serializers
from words.models.collection import Collection

from django.core.validators import MinValueValidator


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["uuid", "created_at", "updated_at", "lang", "index", "nbr_words"]

    nbr_words = serializers.IntegerField(
        source="definitions.count", read_only=True, validators=[MinValueValidator(0)]
    )

    def update(self, instance: Collection, validated_data):
        if validated_data["lang"] != instance.lang:
            same_lang_instance = (
                Collection.objects.filter(
                    user__id=self.context["request"].user.id,
                    lang=validated_data["lang"],
                )
                .exclude(id=instance.id)
                .first()
            )

            if same_lang_instance:
                raise serializers.ValidationError(
                    f"Collection \"{validated_data['lang']}\" already exists"
                )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def create(self, validated_data):
        user = self.context["request"].user

        existing_collection = Collection.objects.filter(
            user__id=self.context["request"].user.id, lang=validated_data["lang"]
        )

        if existing_collection and not existing_collection.delete:
            raise serializers.ValidationError(
                f"Collection \"{validated_data['lang']}\" already exists"
            )

        if existing_collection:
            instance = existing_collection
            instance.deleted = False

            for prop, value in validated_data.items():
                setattr(instance, prop, value)
        else:
            instance = Collection(**validated_data)

        user = self.context["request"].user
        instance.user = user
        instance.save()
        validated_data["uuid"] = instance.uuid

        return instance
