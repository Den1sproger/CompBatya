from django.urls import path
from .views import ServicesAPIList, SpecialistsAPIList, CreateRequest


urlpatterns = [
    path('specialists/<slug:profile>/', SpecialistsAPIList.as_view()),
    path('services/<slug:profile>/', ServicesAPIList.as_view()),
    path('request/', CreateRequest.as_view())
]