from rest_framework import serializers

from routine.Model.Result import Result
from routine.Model.Routine import Routine
from routine.Model.RoutineResult import RoutineResult

class RoutineIDSerializer(serializers.ModelSerializer):
    routine_id = serializers.IntegerField()

    class Meta:
        model  = Routine
        fields = ['routine_id']

class RoutineSerializer(serializers.ModelSerializer):
    routine_id = serializers.IntegerField()
    title      = serializers.CharField(max_length = 100)

    class Meta:
        model  = Routine
        fields = ['routine_id', 'title']
    
class ResultSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 100)

    class Meta:
        model  = Result
        fields = ['title']

class RoutineResultSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer()
    result  = ResultSerializer()

    class Meta:
        model  = RoutineResult
        fields = ['routine', 'result']