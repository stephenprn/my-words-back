from rest_framework import serializers
from words.models.quiz import Quiz, QuizQuestion, QuizQuestionProposal, QuizStatus
from words.models.word_definition import WordDefinition
from words.serializers.quiz_question import QuizQuestionSerializer
import random
from django.core.validators import MinValueValidator, MaxValueValidator


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "duration_limit",
            "nbr_proposals",
            "nbr_questions",
            "nbr_right_answers",
            "status",
        ]

    # 30 seconds is the default
    duration_limit = serializers.IntegerField(
        default=30 * 1000, validators=[MinValueValidator(1)]
    )
    nbr_proposals = serializers.IntegerField(
        default=4, validators=[MinValueValidator(2), MaxValueValidator(10)]
    )
    nbr_questions = serializers.IntegerField(
        default=10, validators=[MinValueValidator(1), MaxValueValidator(50)]
    )

    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status = serializers.ChoiceField(
        choices=QuizStatus.choices, read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user

        # for now, we take 100 random defintions
        # definitions will be used to generate questions and proposals
        word_definitions = (
            WordDefinition.objects.filter(
                user__id=user.id).order_by("?").all()[:100]
        )

        if len(word_definitions) < validated_data["nbr_questions"]:
            raise serializers.ValidationError(
                f"Cannot create a quiz with {validated_data['nbr_questions']} questions with only {len(word_definitions)} definitions saved"
            )

        if len(word_definitions) < validated_data["nbr_proposals"]:
            raise serializers.ValidationError(
                f"Cannot create a quiz with {validated_data['nbr_proposals']} proposals with only {len(word_definitions)} definitions saved"
            )

        instance = Quiz(**validated_data)
        instance.user = user
        instance.save()

        for question_index, word_definition_question in enumerate(
            word_definitions[: instance.nbr_questions], 1
        ):
            wrong_proposals = [
                wd for wd in word_definitions if wd.id != word_definition_question.id
            ]

            question = QuizQuestion(index=question_index)
            question.quiz = instance
            question.save()

            proposals_order = list(range(1, instance.nbr_proposals + 1))
            random.shuffle(proposals_order)

            proposals = [
                QuizQuestionProposal(
                    word_definition=word_definition_question,
                    right_answer=True,
                    question=question,
                    index=proposals_order[0],
                )
            ] + [
                QuizQuestionProposal(
                    word_definition=wrong_answer,
                    question=question,
                    index=proposals_order[proposal_index],
                )
                for proposal_index, wrong_answer in enumerate(
                    random.sample(wrong_proposals,
                                  instance.nbr_proposals - 1), 1
                )
            ]
            proposals = sorted(proposals, key=lambda p: p.index)

            question.proposals.set(
                QuizQuestionProposal.objects.bulk_create(proposals))

        instance.save()
        validated_data["uuid"] = instance.uuid

        return instance


class QuizDetailSerializer(QuizSerializer):
    class Meta:
        model = Quiz
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "duration_limit",
            "nbr_proposals",
            "nbr_questions",
            "nbr_right_answers",
            "status",
            "questions",
        ]

    questions = QuizQuestionSerializer(many=True, read_only=True)
