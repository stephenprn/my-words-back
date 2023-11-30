from rest_framework import serializers

from words.models.quiz import QuizQuestion
from words.serializers.quiz_question_proposal import QuizQuestionProposalSerializer
from django.core.validators import MinValueValidator


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ["uuid", "response_duration", "response_index", "proposals", "index"]

    uuid = serializers.UUIDField(read_only=True)
    proposals = QuizQuestionProposalSerializer(many=True, read_only=True)
    index = serializers.IntegerField(read_only=True, validators=[MinValueValidator(1)])
    response_duration = serializers.IntegerField(
        read_only=True, validators=[MinValueValidator(1)]
    )
    response_index = serializers.IntegerField(
        read_only=True, validators=[MinValueValidator(1)]
    )
