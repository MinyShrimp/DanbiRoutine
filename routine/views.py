import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models      import Quiz
from .serializers import QuizSerializer

# Create your views here.
@api_view(['GET'])
def helloAPI(request):
    return Response('hello world!')

@api_view(['GET'])
def randomQuiz(request, id):
    total_quizs  = Quiz.objects.all()
    random_quizs = random.sample(list(total_quizs), id)
    serializer   = QuizSerializer(random_quizs, many=True)
    return Response(serializer.data)