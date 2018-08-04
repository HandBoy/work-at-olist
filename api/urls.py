from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from .views import CallViewSet, CalculateCallViewSet, CreateCallViewSet, EndCallViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'startcall', CallViewSet, base_name='startcall')
router.register(r'createcall', CreateCallViewSet, base_name='createcall')
router.register(r'endcall', EndCallViewSet, base_name='endcall')
router.register(r'calculatecall', CalculateCallViewSet, base_name='calculatecall')
app_name = 'api'

urlpatterns = [
    url(r'^', include(router.urls)),

]

#    url(r'endcall', EndCallViewSet.as_view({"get": "retrieve", "post": "create", "put": "update", "patch": "partial_update", "delete": "destroy"}), {'get': 'list', 'post': 'create'}),