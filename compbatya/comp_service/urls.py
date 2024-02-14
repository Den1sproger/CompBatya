from django.urls import path
from .views import *



urlpatterns = [
    path('specialists/', SpecialistsAPIList.as_view(), name='specialists-all'),
    path('services/', ServicesAPIList.as_view(), name='services-all'),
    path('devices/', DevicesAPIList.as_view(), name='devices-all'),
    path('clients/', CreateClient.as_view(), name='create-client'),
    path('requests/', RequestsApiList.as_view(), name='requests-all'),
    path('specialists/<slug:profile>/', SpecialistsAPIList.as_view(), name='specialists'),
    path('services/<slug:profile>/', ServicesAPIList.as_view(), name='services'),
    path('create-request/', CreateRequest.as_view(), name='create-request'),
    path('request/<int:pk>/', DeleteUpdateRequest.as_view(), name='request'),
    path('device/', CreateDevice.as_view(), name='create-device'),
    path('device/<int:pk>', UpdateDevice.as_view(), name='update-device'),
]