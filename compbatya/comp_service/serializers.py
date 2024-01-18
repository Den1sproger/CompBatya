from rest_framework import serializers
from .models import Services, Specialists, Requests, Devices



class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('name', 'profile', 'price')



class SpecialistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialists
        fields = ('first_name', 'last_name', 'profile')



class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'

    
    def create(self, validated_data):
        return Requests.objects.create(**validated_data)
    


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        depth = 1
        fields = '__all__'


    def create(self, validated_data):
        return Devices.objects.create(**validated_data)