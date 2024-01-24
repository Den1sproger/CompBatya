from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from .models import Services, Specialists, Requests
from .serializers import *



class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
    


class ServicesAPIList(generics.ListAPIView):
    """View the all services"""

    serializer_class = ServicesSerializer
    pagination_class = SmallResultSetPagination


    def get_queryset(self):
        profile = self.kwargs.get('profile')
        if profile:
            return Services.objects.filter(profile=profile)
        return Services.objects.all()



class SpecialistsAPIList(generics.ListAPIView):
    """View the all specialists"""

    serializer_class = SpecialistsSerializer
    pagination_class = SmallResultSetPagination


    def get_queryset(self):
        profile = self.kwargs.get('profile')
        if profile:
            return Specialists.objects.filter(profile__contains=Specialists.PROFILE_CHOICES[profile])
        return Specialists.objects.all()
    


class RequestsApiList(generics.ListAPIView):
    """View the all requests for a callback"""

    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer
    pagination_class = SmallResultSetPagination

    

class CreateRequest(generics.CreateAPIView):
    """Create the request for a callback from client"""

    serializer_class = RequestsSerializer
    

    def post(self, request):
        serializer = RequestsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(
            data={
                'msg': 'request successfully created',
                'device': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return response
    


class DeleteRequest(generics.DestroyAPIView):
    """Delete the request for a callback in the admin panel"""

    serializer_class = RequestsSerializer
    permission_classes = (IsAdminUser,)


    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method DELETE is not allowed"})
        
        instance = Requests.objects.get(pk=pk).exists()
        if not instance:
            return Response({"error": "Object does not exists"})

        instance.delete()
        return Response({'msg': f'Successfully delete request with pk={pk}'})
    


class DevicesAPIList(generics.ListAPIView):
    """View the all devices that were repaired at the service center"""

    serializer_class = DevicesSerializer
    pagination_class = SmallResultSetPagination
    permission_classes = (IsAdminUser,)
    queryset = Devices.objects.all()



class CreateDevice(generics.CreateAPIView):
    """Create new device that will be repaired"""
    
    serializer_class = DevicesSerializer
    permission_classes = (IsAdminUser,)


    def post(self, request):
        serializer = DevicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(
            data={
                'msg': 'device successfully created',
                'device': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return response
    


class UpdateDevice(generics.UpdateAPIView):
    """Update device status on the success or the fail"""

    serializer_class = DevicesSerializer
    permission_classes = (IsAdminUser,)


    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PATCH is not allowed'})
        
        try:
            instance = Devices.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})
        
        serializer = DevicesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'msg': 'device successfully updated',
            'device': serializer.data
        })