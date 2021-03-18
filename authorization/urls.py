from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^bank-manager-register/$', apis.BankManagerRegistrationView.as_view(),
        name="bank-manager-register"),
    url(r'^register/$', apis.UserRegistrationView.as_view(),
        name="customer-register"),
    url(r'^login/$', apis.LoginView.as_view(), name="user-login"),
    url(r'^profile-with-balance', apis.AccountBalance.as_view(),
        name='profile-with-balance'),
]
