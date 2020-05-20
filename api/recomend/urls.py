from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('questions/', QuestionAPI.as_view()),
    path('answers/', AnswersAPI.as_view()),
]

