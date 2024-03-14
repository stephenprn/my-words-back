from djoser.serializers import UserSerializer
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model

from words.serializers.collection import CollectionSerializer
from words.serializers.word_tag import WordTagSerializer

UserModel = get_user_model()

class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = [
            "email",
            "collections",
            "lang_code",
            "tags"
        ]

    collections = CollectionSerializer(many=True)
    tags = serializers.SerializerMethodField()

    def get_tags(self, instance):
        tags = instance.tags.all().order_by('slug')
        return WordTagSerializer(tags, many=True).data