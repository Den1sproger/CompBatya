from rest_framework import serializers
from .models import Services, Specialists, Requests



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
        fields = ('manager', 'client', 'time')

    
    def create(self, validated_data):
        return Requests.objects.create(**validated_data)