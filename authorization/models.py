from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Sum

from rest_framework_jwt.settings import api_settings

from authorization.managers import UserManager

from transact.models import UserTransaction


class DatabaseCommonFields(models.Model):
    created_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser):
    """
        model to store user infomation
    """
    first_name = models.CharField(
        max_length=50, null=True, blank=True)
    password = models.CharField(max_length=128)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        max_length=254, db_index=True, unique=True)
    username = models.CharField(
        max_length=30, unique=True, db_index=True)
    is_bank_manager = models.BooleanField(default=False)
    customer_acc_no = models.CharField(
        max_length=100, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    @property
    def get_current_bank_balance(self):
        credit_aggs = UserTransaction.objects.filter(
            user__id=self.id,
            is_debit=False
        ).aggregate(total=Sum('amount'))

        debit_aggs = UserTransaction.objects.filter(
            user__id=self.id,
            is_debit=True
        ).aggregate(total=Sum('amount'))

        credit_amount = credit_aggs.get('total')
        credit_amount = credit_amount if credit_amount is not None else 0.0

        debit_amount = debit_aggs.get('total')
        debit_amount = debit_amount if debit_amount is not None else 0.0

        return credit_amount - debit_amount

    def get_jwt_token_for_user(self):
        """ get jwt token for the user """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self)
        payload.update({
            "is_bank_manager": self.is_bank_manager,
            "first_name": self.first_name,
            "last_name": self.last_name,
        })
        token = jwt_encode_handler(payload)
        return token

    class Meta:
        def __str__(self):
            return self.get_full_name()
