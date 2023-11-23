from django.urls import path
from words import views
from rest_framework.routers import DefaultRouter
from words.views.words import WordDefinitionViewSet

router = DefaultRouter()
router.register('definitions', WordDefinitionViewSet, basename="WordDefinitionViewSet")

urlpatterns = router.urls