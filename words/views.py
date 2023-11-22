from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def say_hello(request):
    return Response()