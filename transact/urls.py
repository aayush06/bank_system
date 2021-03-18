from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()
router.register(r"account-transaction", apis.CustomerTransactView,
                base_name="account-transaction")

urlpatterns = [
    url(r'^', include(router.urls)),
]
