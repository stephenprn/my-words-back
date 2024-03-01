from rest_framework import serializers
from words.models.word_tag import WordTag
from words.utils.string import slugify


class WordTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordTag
        fields = [
            "uuid",
            "label",
            "emoji",
            "slug",
        ]

    slug = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)

    def update(self, instance: WordTag, validated_data):
        slug = slugify(validated_data["label"])
        user_id = self.context["request"].user.id

        validated_data["slug"] = slug

        if slug != instance.slug:
            same_slug_instace = (
                WordTag.objects.filter(user__id=user_id, slug=slug)
                .exclude(id=instance.id)
                .first()
            )

            if same_slug_instace:
                raise serializers.ValidationError(
                    f"Tag with label \"{validated_data['label']}\" already exists"
                )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def create(self, validated_data):
        slug = slugify(validated_data["label"])
        user_id = self.context["request"].user.id

        validated_data["slug"] = slug

        existing_tag = WordTag.objects.filter(user__id=user_id, slug=slug).first()

        if existing_tag and not existing_tag.deleted:
            raise serializers.ValidationError(
                f"Tag with label \"{validated_data['label']}\" already exists"
            )

        if existing_tag:
            instance = existing_tag
            instance.deleted = False

            for prop, value in validated_data.items():
                setattr(instance, prop, value)
        else:
            instance = WordTag(**validated_data)

        user = self.context["request"].user
        instance.user = user

        instance.save()
        validated_data["uuid"] = instance.uuid

        return instance
