from rest_framework import serializers
from routine.Model.Message import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Message
        fields = ('msg', 'status')