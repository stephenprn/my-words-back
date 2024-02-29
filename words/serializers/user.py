from djoser.serializers import UserSerializer
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model

from words.serializers.collection import CollectionSerializer

UserModel = get_user_model()

class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = [
            "email",
            "collections",
            "lang_code"
        ]

    collections = CollectionSerializer(many=True)
