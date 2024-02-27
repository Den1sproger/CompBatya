from django.core.cache import cache
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Services, Specialists, Requests, Owners
from .serializers import *
from .permissions import IsAdmin
from .tasks import send_mail_to_managers



class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    


class ServicesAPIList(generics.ListAPIView):
    """View the all services"""

    serializer_class = ServicesSerializer
    pagination_class = SmallResultSetPagination


    def get_queryset(self):
        profile = self.kwargs.get('profile')
        if profile:
            result = cache.get(f'services_{profile}')
            if not result:
                result = Services.objects.filter(profile=profile)
                cache.set(f'services_{profile}', result, 60 * 60)
            return result
        
        result = cache.get('services')
        if not result:
            result = Services.objects.all()
            cache.set('services', result, 60 * 60)

        return result
    


class SpecialistsAPIList(generics.ListAPIView):
    """View the all specialists"""

    serializer_class = SpecialistsSerializer
    pagination_class = SmallResultSetPagination


    def get_queryset(self):
        profile = self.kwargs.get('profile')
        if profile:
            result = cache.get(f'specialists_{profile}')
            if not result:
                result = Specialists.objects.filter(profile__contains=Specialists.PROFILE_CHOICES[profile])
                cache.set(f'specialists_{profile}', result, 60 * 60 * 24)
            return result

        result = cache.get('specialists')
        if not result:
            result = Specialists.objects.all()
            cache.set('specialists', result, 60 * 60)

        return result
    


class RequestsApiList(generics.ListAPIView):
    """View the all requests for a callback"""

    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer
    pagination_class = SmallResultSetPagination
    permission_classes = (IsAdmin,)

    

class CreateClient(generics.CreateAPIView):
    """Create the new client"""

    serializer_class = ClientsSerializer


    def post(self, request):
        phone = request.data['phone_number']
        name = request.data['name']
        try:
            client_mail = request.data['email']
        except KeyError:
            client_mail = None

        serializer = ClientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            client = Owners.objects.get(
                Q(phone_number=phone) | (Q(email=client_mail) & Q(email__isnull=False))
            )
            if client:
                client.requests.create()
            else:
                return Response(
                    data={'msg': 'Bad request'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        send_mail_to_managers.delay(phone, name, client_mail)

        response = Response(
            data={
                'msg': 'client successfully created',
                'client': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return response

    

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
                'request': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        return response
    


class DeleteUpdateRequest(APIView):
    """Delete and Update the request for a callback in the admin panel"""

    serializer_class = RequestsSerializer
    permission_classes = (IsAdmin,)


    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response(
                data={"error": "Method PATCH is not allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        try:
            instance = Requests.objects.get(pk=pk)
        except:
            return Response(
                data={"error": "Object does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RequestsSerializer(data=request.data,
                                        instance=instance,
                                        partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'msg': 'Request successfully updated',
            'request': serializer.data
        })


    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response(
                data={"error": "Method DELETE is not allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        try:
            instance = Requests.objects.get(pk=pk)
        except:
            return Response(
                data={"error": "Object does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        instance.delete()
        return Response({'msg': f'Successfully delete request with pk={pk}'})
    


class DevicesAPIList(generics.ListAPIView):
    """View the all devices that were repaired at the service center"""

    serializer_class = DevicesSerializer
    pagination_class = SmallResultSetPagination
    permission_classes = (IsAdmin,)
    queryset = Devices.objects.all()



class CreateDevice(generics.CreateAPIView):
    """Create new device that will be repaired"""
    
    serializer_class = DevicesSerializer
    permission_classes = (IsAdmin,)


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
    permission_classes = (IsAdmin,)


    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response(
                data={'error': 'Method PATCH is not allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        try:
            instance = Devices.objects.get(pk=pk)
        except:
            return Response(
                data={"error": "Object does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DevicesSerializer(data=request.data,
                                       instance=instance,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'msg': 'device successfully updated',
            'device': serializer.data
        })