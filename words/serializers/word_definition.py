from rest_framework import serializers
from words.models.word_definition import WordDefinition
from words.utils.string import slugify


class WordDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordDefinition
        fields = ['word', 'definition', 'note', 'uuid', 'example', 'slug']

    slug = serializers.CharField(read_only=True)

    def save(self):
        slug = slugify(self.validated_data['word'])

        if WordDefinition.objects.filter(
            user__id=self.context["request"].user.id,
            slug=slug
        ):
            raise serializers.ValidationError(
                f'A word with slug {slug} already exists'
            )

        word_definition = WordDefinition(**self.validated_data)
        word_definition.slug = slug

        user = self.context["request"].user
        word_definition.user = user
        word_definition.save()
        
        return word_definition