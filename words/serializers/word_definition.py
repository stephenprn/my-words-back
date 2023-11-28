from rest_framework import serializers
from words.models.word_definition import WordDefinition
from words.utils.string import slugify


class WordDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordDefinition
        fields = ["word", "definition", "note", "uuid", "example", "slug"]

    slug = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        slug = slugify(validated_data["word"])

        if slug != instance.slug and WordDefinition.objects.filter(
            user__id=self.context["request"].user.id, slug=slug
        ).exclude(id=instance.id):
            raise serializers.ValidationError(f"A word with slug {slug} already exists")

        validated_data["slug"] = slug

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def create(self, validated_data):
        slug = slugify(validated_data["word"])

        if WordDefinition.objects.filter(
            user__id=self.context["request"].user.id, slug=slug
        ):
            raise serializers.ValidationError(f"A word with slug {slug} already exists")

        validated_data["slug"] = slug
        instance = WordDefinition(**validated_data)

        user = self.context["request"].user
        instance.user = user
        instance.save()
        validated_data["uuid"] = instance.uuid

        return instance
