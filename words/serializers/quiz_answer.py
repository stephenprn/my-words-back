from rest_framework import serializers
from django.core.validators import MinValueValidator


class QuizAnswerSerializer(serializers.Serializer):
    question_index = serializers.IntegerField(validators=[MinValueValidator(1)])
    response_index = serializers.IntegerField(allow_null=True, validators=[MinValueValidator(1)])
    response_duration = serializers.IntegerField(validators=[MinValueValidator(1)])


class QuizAnswersSerializer(serializers.Serializer):
    answers = QuizAnswerSerializer(many=True)

    def validate_answers(self, answers):
        if len(answers) < 1:
            raise serializers.ValidationError("Specify at least one answer")

        return answers