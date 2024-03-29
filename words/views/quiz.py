from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.response import Response
from rest_framework import status
from words.models.quiz import Quiz, QuizQuestion, QuizStatus
from words.serializers.quiz import (
    QuizDetailSerializer,
    QuizInputSerializer,
    QuizSerializer,
)
from words.serializers.quiz_answer import QuizAnswersSerializer
from rest_framework.decorators import action

from words.utils.quiz import compute_nbr_right_answers, compute_status


class QuizViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action == "answer":
            return QuizAnswersSerializer

        if self.action == "list":
            return QuizSerializer

        if self.action == "create":
            return QuizInputSerializer

        return QuizDetailSerializer

    def get_queryset(self):
        queryset = Quiz.objects.filter(user__id=self.request.user.id)

        if self.request.query_params.get("statusIn"):
            statuses = []

            for status_str in self.request.query_params.get("statusIn").split(","):
                if status_str not in QuizStatus:
                    continue

                statuses.append(QuizStatus[status_str])

            if statuses:
                queryset = queryset.filter(status__in=statuses)

        queryset = queryset.order_by("-created_at", "id")

        return queryset.all()

    def get_serializer_context(self):
        return {"request": self.request}

    @action(methods=["post"], detail=True)
    def answer(self, request, uuid):
        SerializerClass = self.get_serializer_class()

        serializer = SerializerClass(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create a map and remove potential duplicates in question_uuid
        answers_responses_map = {
            answer["question_index"]: {
                "response_index": answer["response_index"],
                "response_duration": answer["response_duration"],
            }
            for answer in serializer.data["answers"]
        }

        quiz = (
            Quiz.objects.filter(uuid=uuid, user__id=self.request.user.id)
            .prefetch_related("questions", "questions__proposals")
            .first()
        )

        if not all(
            [q_index <= quiz.nbr_questions for q_index in answers_responses_map.keys()]
        ):
            return Response(
                {
                    "detail": f"Questions with following indexes were not found: {', '.join(str(q_index) for q_index in answers_responses_map.keys() if q_index > quiz.nbr_questions)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check all response_indexes are correct
        if not all(
            [
                r["response_index"] is None or r["response_index"] <= quiz.nbr_proposals
                for r in answers_responses_map.values()
            ]
        ):
            return Response(
                {
                    "detail": f"Responses with following indexes were not found: {', '.join(str(r['response_index']) for r in answers_responses_map.values() if r['response_index'] > quiz.nbr_proposals)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions_map = {question.index: question for question in quiz.questions.all()}

        for question_index, response_data in answers_responses_map.items():
            question = questions_map[question_index]

            question.response_duration = response_data["response_duration"]
            question.response_index = response_data["response_index"]

        QuizQuestion.objects.bulk_update(
            list(questions_map.values()), ["response_duration", "response_index"]
        )

        quiz.status = compute_status(quiz)
        quiz.nbr_right_answers = compute_nbr_right_answers(quiz)
        quiz.save()

        return Response(QuizDetailSerializer(quiz).data)
