from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from words.models.quiz import Quiz
from words.serializers.quiz import QuizSerializer


class QuizViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = QuizSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Quiz.objects.filter(user__id=self.request.user.id).all()
        return queryset

    def get_serializer_context(self):
        return {"request": self.request}
