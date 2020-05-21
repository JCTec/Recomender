import json
from common.ContentKNN import ContentKNN
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


class QuestionAPI(APIView):

    def get(self, request):
        try:
            courses = Question.objects.all()
            serializer = QuestionSerializer(courses, many=True)

            return Response(dict(status="Success", data=serializer.data))
        except Exception as e:
            return Response(dict(status="Error", errors=['Not found', str(e)]), status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnswersAPI(APIView):

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            answers = data["quiz"]
            questions = Question.objects.filter(id__in=answers)
            tags = {questions.get(pk=key).tag.name: val for key, val in answers.items()}
            History(value=json.dumps(tags)).save()
            knn = ContentKNN()
            
            return Response(dict(status="Success", data=knn.predict(tags)))
        except Exception as e:
            return Response(dict(status="Error", errors=['Not found', str(e)]), status.HTTP_500_INTERNAL_SERVER_ERROR)


