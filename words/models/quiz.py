from django.conf import settings
from django.db import models
from common.models.timestamped import TimestampedModelMixin
from common.models.uuid import UuidModelMixin
from words.models.word_definition import WordDefinition


class Quiz(TimestampedModelMixin, UuidModelMixin):
    duration_limit = models.BigIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    response_duration = models.BigIntegerField(null=True)


class QuizQuestionProposal(TimestampedModelMixin):
    question = models.ForeignKey(
        QuizQuestion, related_name="proposals", on_delete=models.CASCADE
    )
    right_answer = models.BooleanField(default=False)
    word_definition = models.ForeignKey(
        WordDefinition,
        null=True,
        related_name="quiz_question_proposals",
        on_delete=models.SET_NULL,
    )
