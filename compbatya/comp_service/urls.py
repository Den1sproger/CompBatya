from django.urls import path
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register('devices', DevicesViewSet)
router.register('requests', RequestsViewSet)


urlpatterns = [
    path('specialists/', SpecialistsAPIList.as_view(), name='specialists-all'),
    path('services/', ServicesAPIList.as_view(), name='services-all'),
    path('clients/', CreateClient.as_view(), name='create-client'),
    path('specialists/<slug:profile>/', SpecialistsAPIList.as_view(), name='specialists'),
    path('services/<slug:profile>/', ServicesAPIList.as_view(), name='services'),
]

urlpatterns += router.urls