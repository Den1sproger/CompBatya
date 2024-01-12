from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Services, Specialists
from .serializers import *


# Create your views here.

class ServicesAPIList(generics.ListAPIView):
    serializer_class = ServicesSerializer

    def get_queryset(self):
        profile = self.kwargs.get('profile')
        return Services.objects.filter(profile=profile)



class SpecialistsAPIList(generics.ListAPIView):
    serializer_class = SpecialistsSerializer

    def get_queryset(self):
        profile = self.kwargs.get('profile')
        return Specialists.objects.filter(profile__contains=Specialists.PROFILE_CHOICES[profile])
    


class CreateRequest(generics.CreateAPIView):
    serializer_class = RequestsSerializer
    
    def post(self, request):
        serializer = RequestsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'request': serializer.data})