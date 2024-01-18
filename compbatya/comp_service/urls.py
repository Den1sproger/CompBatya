from django.urls import path
from .views import *



urlpatterns = [
    path('specialists/', SpecialistsAPIList.as_view()),
    path('services/', ServicesAPIList.as_view()),
    path('devices/', DevicesAPIList.as_view()),
    path('specialists/<slug:profile>/', SpecialistsAPIList.as_view()),
    path('services/<slug:profile>/', ServicesAPIList.as_view()),
    path('request/', CreateRequest.as_view()),
    path('request/delete/<int:pk>/', DeleteRequest.as_view()),
    path('device/', CreateDevice.as_view()),
]