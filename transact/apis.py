from datetime import datetime
import pytz

from rest_framework import (permissions, response, status,
                            viewsets, exceptions, views)
from rest_framework.viewsets import mixins

from authorization.models import User
from helpers.email import EmailHandler
from helpers.excel_generator import ExcelGenerator
from helpers.permissions import AdminOnly
from transact.models import UserTransaction
from transact.serializers import (UserAccountTransactSerializer,
                                  ExportSerializer)

email_handler = EmailHandler()
excel_generator = ExcelGenerator()


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
            serializer.save()
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


class ManagerReportView(views.APIView):
    """
        Give list of ids to download particular
    """
    model = UserTransaction
    permission_classes = (permissions.IsAuthenticated, AdminOnly)
    serializer_class = ExportSerializer

    def get_queryset(self, user_id=[]):
        """ get query set """
        start_timestamp = self.request.data.get('start_timestamp', None)
        end_timestamp = self.request.data.get('end_timestamp', None)

        if isinstance(start_timestamp, str):
            start_timestamp = datetime.strptime(
                start_timestamp, "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=pytz.UTC)
        if isinstance(end_timestamp, str):
            end_timestamp = datetime.strptime(
                end_timestamp, "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=pytz.UTC)
        user_trans_qs = self.model.objects.filter(
            timestamp__gte=start_timestamp, timestamp__lte=end_timestamp,
            user__id__in=user_id
        )
        return user_trans_qs.order_by('-timestamp')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data.get('select_all') is True:
                user_id = User.objects.filter(
                    is_bank_manager=False, is_active=True).values_list(
                        'id', flat=True)
                objects = self.get_queryset(user_id=list(user_id))
            elif serializer.validated_data.get('select_all') is False:
                user_id = request.data.get('ids', [])
                objects = self.get_queryset(user_id=user_id)
            object_id = [data.id for data in objects]
            file_path = excel_generator.run(
                            object_id, user_id=user_id)
            if file_path:
                file_path = file_path.split("/bank_system")[1]
            return response.Response(
                {'file_path': file_path},
                status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
