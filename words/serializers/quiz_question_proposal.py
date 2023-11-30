from rest_framework import serializers

from words.models.quiz import QuizQuestionProposal
from words.serializers.word_definition import WordDefinitionSerializer
from django.core.validators import MinValueValidator


class QuizQuestionProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestionProposal
        fields = ["right_answer", "word_definition", "index"]

    word_definition = WordDefinitionSerializer()
    index = serializers.IntegerField(read_only=True, validators=[MinValueValidator(1)])
