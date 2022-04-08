from rest_framework import serializers
from routine.Model.Routine import Routine

class RoutineSerializer(serializers.ModelSerializer):
    routine_id = serializers.IntegerField()

    class Meta:
        model  = Routine
        fields = ('routine_id')