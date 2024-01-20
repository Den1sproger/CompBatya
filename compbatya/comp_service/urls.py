from django.urls import path
from .views import *



urlpatterns = [
    path('specialists/', SpecialistsAPIList.as_view(), name='specialists-all'),
    path('services/', ServicesAPIList.as_view(), name='services-all'),
    path('devices/', DevicesAPIList.as_view(), name='devices-all'),
    path('specialists/<slug:profile>/', SpecialistsAPIList.as_view(), name='specialists'),
    path('services/<slug:profile>/', ServicesAPIList.as_view(), name='services'),
    path('request/', CreateRequest.as_view(), name='create-request'),
    path('request/delete/<int:pk>/', DeleteRequest.as_view()),
    path('device/', CreateDevice.as_view(), name='create-device'),
    path('device/<int:pk>', UpdateDevice.as_view(), name='update-device'),
]