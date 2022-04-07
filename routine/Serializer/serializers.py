from rest_framework import serializers
from ..Model.Message import Message
from ..Model.Account import Account

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Message
        fields = ('msg', 'status')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Account
        fields = ('msg', 'status')