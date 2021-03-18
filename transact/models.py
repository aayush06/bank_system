from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class DatabaseCommonFields(models.Model):
    created_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserTransaction(DatabaseCommonFields):
    user = models.ForeignKey(
        "authorization.User", null=True, blank=True,
        on_delete=models.CASCADE, related_name="customer")
    is_debit = models.BooleanField(default=True)
    timestamp = models.DateTimeField(
        auto_now=True, null=True, blank=True
    )
    amount = models.FloatField()
