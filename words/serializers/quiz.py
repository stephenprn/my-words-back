from rest_framework import serializers
from words.models.quiz import Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "duration_limit",
            "questions__response_duration",
            "questions__proposals__right_answer",
            "questions__proposals__word_definition__word",
            "questions__proposals__word_definition__definition",
            "questions__proposals__word_definition__slug",
            "questions__proposals__word_definition__uuid",
        ]

    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
