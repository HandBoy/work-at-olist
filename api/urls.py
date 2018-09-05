from django.conf.urls import include, url
from rest_framework import routers

from .views import (CreateCallViewSet, EndCallViewSet, MonthlyBillingView)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^call/start/$', CreateCallViewSet.as_view()),
    url(r'^call/(?P<id>[0-9]+)/end/$', EndCallViewSet.as_view()),
    url(r'^bills/(?P<phone_number>[0-9]+)/$', MonthlyBillingView.as_view())
]
