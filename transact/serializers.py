from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

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
