from rest_framework import serializers
from words.models.collection import Collection
from words.models.word_definition import WordDefinition
from words.utils.string import slugify


class WordDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordDefinition
        fields = [
            "word",
            "definition",
            "note",
            "uuid",
            "example",
            "slug",
            "collection_lang",
        ]

    slug = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    collection_lang = serializers.CharField(source="collection.lang")

    def update(self, instance: WordDefinition, validated_data):
        slug = slugify(validated_data["word"])
        user_id = self.context["request"].user.id

        validated_data["slug"] = slug

        collection_input = validated_data.pop("collection")
        collection_lang = collection_input["lang"]

        if slug != instance.slug:
            same_slug_instace = (
                WordDefinition.objects.filter(
                    user__id=user_id, collection__lang=collection_lang, slug=slug
                )
                .exclude(id=instance.id)
                .first()
            )

            if same_slug_instace:
                raise serializers.ValidationError(
                    f"Word \"{validated_data['word']}\" already exists"
                )

        if collection_lang != instance.collection.lang:
            collection = Collection.objects.filter(
                user__id=user_id, lang=collection_lang
            ).first()

            if not collection:
                raise serializers.ValidationError(
                    f'Collection "{collection_lang}" not found'
                )

            instance.collection = collection

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def create(self, validated_data):
        slug = slugify(validated_data["word"])
        user_id = self.context["request"].user.id

        validated_data["slug"] = slug

        collection_input = validated_data.pop("collection")
        collection_lang = collection_input["lang"]

        existing_word = WordDefinition.objects.filter(
            user__id=user_id, collection__lang=collection_lang, slug=slug
        ).first()

        if existing_word and not existing_word.deleted:
            raise serializers.ValidationError(
                f"Word \"{validated_data['word']}\" already exists"
            )

        collection = Collection.objects.filter(
            user__id=user_id, lang=collection_lang
        ).first()

        if not collection:
            raise serializers.ValidationError(
                f'Collection "{collection_lang}" not found'
            )

        if existing_word:
            instance = existing_word
            instance.deleted = False

            for prop, value in validated_data.items():
                setattr(instance, prop, value)
        else:
            instance = WordDefinition(**validated_data)

        instance.collection = collection

        user = self.context["request"].user
        instance.user = user

        instance.save()
        validated_data["uuid"] = instance.uuid

        return instance
