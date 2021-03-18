from rest_framework import (permissions, response, status,
                            viewsets, exceptions)
from rest_framework.viewsets import mixins

from helpers.email import EmailHandler
from transact.models import UserTransaction
from transact.serializers import UserAccountTransactSerializer

email_handler = EmailHandler()


class CustomerTransactView(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """ Endpoint for customer transactions """
    http_method_names = ["get", "post"]
    permission_classes = (permissions.IsAuthenticated,)
    model = UserTransaction
    serializer_class = UserAccountTransactSerializer
    queryset = UserTransaction.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user.id
        request.data.update({
            'user': user
        })
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            ctx = dict()
            if serializer.validated_data.get('is_debit'):
                ctx['action'] = 'debited'
            else:
                ctx['action'] = 'credited'
            ctx['name'] = request.user.first_name + ' ' + request.user.last_name
            ctx['amount'] = serializer.validated_data['amount']
            ctx['email'] = request.user.email
            email_handler.create_email(**ctx)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
