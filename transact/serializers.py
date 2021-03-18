from rest_framework import serializers

from authorization.models import User
from transact.models import UserTransaction


class UserAccountTransactSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(
        required=True
    )
    is_debit = serializers.BooleanField(
        required=True
    )

    class Meta:
        model = UserTransaction
        fields = '__all__'


class ExportSerializer(serializers.ModelSerializer):
    ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False)
    select_all = serializers.BooleanField(default=False)
    start_timestamp = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], required=True
    )
    end_timestamp = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], required=True
    )

    class Meta:
        model = UserTransaction
        fields = ('ids', 'select_all', 'start_timestamp', 'end_timestamp')
