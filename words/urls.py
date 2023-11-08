from django.urls import path
from words import views

urlpatterns = [
    path('hello', views.say_hello)
]