from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Services, Specialists, Requests
from .serializers import *



class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
    


class ServicesAPIList(generics.ListAPIView):
    serializer_class = ServicesSerializer
    pagination_class = SmallResultSetPagination

    def get_queryset(self):
        profile = self.kwargs.get('profile')
        if profile:
            return Services.objects.filter(profile=profile)
        return Services.objects.all()



class SpecialistsAPIList(generics.ListAPIView):
    serializer_class = SpecialistsSerializer
    pagination_class = SmallResultSetPagination

    def get_queryset(self):
        profile = self.kwargs.get('profile')
        if profile:
            return Specialists.objects.filter(profile__contains=Specialists.PROFILE_CHOICES[profile])
        return Specialists.objects.all()
    


class CreateRequest(generics.CreateAPIView):
    serializer_class = RequestsSerializer
    
    def post(self, request):
        serializer = RequestsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'request': serializer.data})