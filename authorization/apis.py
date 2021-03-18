from uuid import uuid4

from rest_framework import (generics, permissions,
                            response, status)

from authorization.serializers import (LoginSerializer,
                                       RegistrationSerializer,
                                       BankManagerRegistrationSerializer)


class LoginView(generics.GenericAPIView):
    """ Endpoint for the user login """

    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            response_dict = dict()
            auth_token = user.get_jwt_token_for_user()
            response_dict["auth_token"] = auth_token
            response_dict["is_bank_manager"] = user.is_bank_manager
            response_dict["id"] = user.id
            response_dict["last_login"] = user.last_login
            response_dict["customer_acc_no"] = user.customer_acc_no
            return response.Response(
                data=response_dict,
                status=status.HTTP_200_OK,
            )


class UserRegistrationView(generics.CreateAPIView):
    """ endpoint to register user """

    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(serializer.validated_data.get("password"))
            user.customer_acc_no = uuid4().hex
            user.save()
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class BankManagerRegistrationView(generics.CreateAPIView):
    """ endpoint to register user """

    permission_classes = (permissions.AllowAny,)
    serializer_class = BankManagerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class AccountBalance(generics.GenericAPIView):
    """ Endpoint for the user current bank balance """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kargs):
        user = request.user
        response_dict = dict()
        response_dict["current_balance"] = user.get_current_bank_balance
        response_dict["name"] = user.first_name + ' ' + user.last_name
        response_dict["email"] = user.email
        response_dict["last_login"] = user.last_login
        response_dict["customer_acc_no"] = user.customer_acc_no
        return response.Response(
            data=response_dict,
            status=status.HTTP_200_OK,
        )