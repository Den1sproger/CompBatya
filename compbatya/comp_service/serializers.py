from rest_framework import serializers
from .models import Services, Specialists, Requests, Devices



class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'



class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'

    
    def create(self, validated_data):
        return Requests.objects.create(**validated_data)
    


class DevicesSerializer(serializers.ModelSerializer):
    # many-to-many fields
    specialists = serializers.PrimaryKeyRelatedField(many=True,
                                                     queryset=Specialists.objects.all())
    services = serializers.PrimaryKeyRelatedField(many=True,
                                                  queryset=Services.objects.all())

    class Meta:
        model = Devices
        depth = 1
        fields = ('id', 'type', 'model', 'year', 'owner', 'status', 'specialists', 'services')


    def create(self, validated_data):
        specialists = validated_data['specialists']
        services = validated_data['services']
        del validated_data['specialists']
        del validated_data['services']

        new_device = Devices.objects.create(**validated_data)
        new_device.specialists.set(specialists)
        new_device.services.set(services)

        return new_device
    

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    


class SpecialistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialists
        fields = '__all__'