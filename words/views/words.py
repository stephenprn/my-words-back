from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from words.models.word_definition import WordDefinition
from words.serializers.word_definition import WordDefinitionSerializer

class WordDefinitionViewSet(ModelViewSet):
	serializer_class = WordDefinitionSerializer
	
	def get_queryset(self):
		queryset = WordDefinition.objects.filter(
			user__id=self.request.user.id
		).all()
		return queryset

	def get_serializer_context(self):
		return { 'request': self.request }

    
	
