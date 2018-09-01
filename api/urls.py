from django.conf.urls import include, url
from rest_framework import routers

from .views import (CreateCallViewSet, EndCallViewSet, MonthlyBillingView)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

app_name = 'api'

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^startcall/$', CreateCallViewSet.as_view(), name='startcall'),
    url(r'^endcall/$', EndCallViewSet.as_view(), name='endcall'),
    url(r'^billing/'
        + '(?P<phone_number>[0-9]+)/$',
        MonthlyBillingView.as_view(), name='get_bill'),
    url(r'^billing/'
        + '(?P<phone_number>[0-9]+)/'
        + '(?P<year>[0-9]{4})/$',
        MonthlyBillingView.as_view(), name='get_bill'),
    url(r'^billing/'
        + '(?P<phone_number>[0-9]+)/'
        + '(?P<year>[0-9]{4})/'
        + '(?P<month>[0-9]{2})/$',
        MonthlyBillingView.as_view(), name='get_bill'),
]
