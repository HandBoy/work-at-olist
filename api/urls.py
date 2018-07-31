from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from .views import CallViewSet, CreateCallViewSet2, CreateCallViewSet, EndCallViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'startcall', CallViewSet, base_name='startcall')
#router.register(r'createcall2', CreateCallViewSet2, base_name='createcall2')
router.register(r'createcall', CreateCallViewSet, base_name='createcall')
router.register(r'endcall', EndCallViewSet, base_name='endcall')
app_name = 'api'

urlpatterns = [
    url(r'^', include(router.urls)),

]

#    url(r'endcall', EndCallViewSet.as_view({"get": "retrieve", "post": "create", "put": "update", "patch": "partial_update", "delete": "destroy"}),