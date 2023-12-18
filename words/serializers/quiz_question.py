from rest_framework import serializers

from words.models.quiz import QuizQuestion, QuizQuestionType
from words.serializers.quiz_question_proposal import QuizQuestionProposalSerializer
from django.core.validators import MinValueValidator


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = [
            "uuid",
            "response_duration",
            "response_index",
            "question_type",
            "proposals",
            "index",
        ]

    uuid = serializers.UUIDField(read_only=True)
    proposals = QuizQuestionProposalSerializer(many=True, read_only=True)
    index = serializers.IntegerField(read_only=True, validators=[MinValueValidator(1)])
    response_duration = serializers.IntegerField(
        read_only=True, validators=[MinValueValidator(1)]
    )
    response_index = serializers.IntegerField(
        read_only=True, validators=[MinValueValidator(1)]
    )
    question_type = serializers.ChoiceField(
        choices=QuizQuestionType.choices, read_only=True
    )
