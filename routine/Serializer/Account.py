from rest_framework import serializers
from routine.Model.Account import Account

class AccountIDSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField()
    class Meta:
        model = Account
        fields = ['account_id']