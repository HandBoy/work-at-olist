from django.conf.urls import url, include
from rest_framework import routers
from .views import CalculateCallViewSet, CreateCallViewSet, EndCallViewSet, MonthlyBillingView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'startcall', CreateCallViewSet, base_name='startcall')
router.register(r'endcall', EndCallViewSet, base_name='endcall')
router.register(r'calculatecall', CalculateCallViewSet, base_name='calculatecall')

app_name = 'api'

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^billing/(?P<phone_number>[0-9]+)/$', MonthlyBillingView.as_view()),   
    url(r'^billing/(?P<phone_number>[0-9]+)/(?P<year>[0-9]{4})/$', MonthlyBillingView.as_view()),
    url(r'^billing/(?P<phone_number>[0-9]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', MonthlyBillingView.as_view()),   
]