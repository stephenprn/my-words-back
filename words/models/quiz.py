from django.conf import settings
from django.db import models
from common.models.timestamped import TimestampedModelMixin
from common.models.uuid import UuidModelMixin
from words.models.collection import Collection
from words.models.word_definition import WordDefinition
from django.core.validators import MinValueValidator


class QuizStatus(models.TextChoices):
    NOT_STARTED = "NOT_STARTED", "NOT_STARTED"
    PARTIALLY_COMPLETE = "PARTIALLY_COMPLETE", "PARTIALLY_COMPLETE"
    COMPLETE = "COMPLETE", "COMPLETE"


class Quiz(TimestampedModelMixin, UuidModelMixin):
    duration_limit = models.PositiveBigIntegerField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        choices=QuizStatus.choices,
        default=QuizStatus.NOT_STARTED,
    )
    nbr_proposals = models.IntegerField(default=4, validators=[MinValueValidator(1)])
    nbr_questions = models.IntegerField(default=10, validators=[MinValueValidator(1)])
    nbr_right_answers = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    collection = models.ForeignKey(
        Collection, related_name="quizes", on_delete=models.CASCADE
    )


class QuizQuestionType(models.TextChoices):
    GUESS_FROM_DEFINITION = "GUESS_FROM_DEFINITION", "GUESS_FROM_DEFINITION"
    GUESS_FROM_WORD = "GUESS_FROM_WORD", "GUESS_FROM_WORD"


class QuizQuestion(UuidModelMixin):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_type = models.CharField(
        choices=QuizQuestionType.choices,
    )

    index = models.IntegerField(validators=[MinValueValidator(1)])

    # null if user timeout
    response_index = models.PositiveIntegerField(
        null=True, validators=[MinValueValidator(1)]
    )
    # null if not answered yet, duration if answered
    response_duration = models.PositiveBigIntegerField(null=True)


class QuizQuestionProposal(TimestampedModelMixin):
    question = models.ForeignKey(
        QuizQuestion, related_name="proposals", on_delete=models.CASCADE
    )
    right_answer = models.BooleanField(default=False)
    index = models.IntegerField(validators=[MinValueValidator(1)])
    word_definition = models.ForeignKey(
        WordDefinition,
        null=True,
        related_name="quiz_question_proposals",
        on_delete=models.SET_NULL,
    )
