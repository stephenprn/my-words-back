from rest_framework.routers import DefaultRouter
from words.views.quiz import QuizViewSet
from words.views.word_definition import WordDefinitionViewSet

router = DefaultRouter()
router.register("definitions", WordDefinitionViewSet, basename="WordDefinitionViewSet")
router.register("quizes", QuizViewSet, basename="QuizViewSet")

urlpatterns = router.urls
