from django.db import models
from common.models.timestamped import TimestampedModelMixin
from common.models.uuid import UuidModelMixin
from words.models.word_definition import WordDefinition


class Quiz(TimestampedModelMixin, UuidModelMixin):
    duration_limit = models.BigIntegerField()

class QuizQuestion(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	response_duration = models.BigIntegerField(null=True)

class QuizQuestionProposal(TimestampedModelMixin):
	question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
	right_answer = models.BooleanField(default=False)
	word_definition = models.ForeignKey(WordDefinition, null=True, on_delete=models.SET_NULL)
