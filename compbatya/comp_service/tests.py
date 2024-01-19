from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import *


class GetDataTestCase(APITestCase):
    fixtures = ['comp_service_brands.json',
                'comp_service_devices.json',
                'comp_service_managers.json',
                'comp_service_models.json',
                'comp_service_owners.json',
                'comp_service_services.json',
                'comp_service_specialists.json']

    
    def setUp(self):
        print('[INFO] Start test')


    def test_get_all_specialists(self):
        url = reverse('specialists-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 10)


    def test_get_all_services(self):
        url = reverse('services-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 10)
        

    def test_get_all_devices(self):
        url = reverse('devices-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 10)


    def test_get_specialists(self):
        profile = 'desktop'
        url = reverse('specialists', args=(profile,))
        response = self.client.get(url)
        result_count = len(response.data['results'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        count = Specialists.objects.filter(profile__contains=Specialists.PROFILE_CHOICES[profile]).count()

        if count < 10:
            self.assertEqual(result_count, count)
        else:
            self.assertLessEqual(result_count, 10)


    def test_get_services(self):
        profile = 'desktop'
        url = reverse('services', args=(profile,))
        print(url)
        response = self.client.get(url)
        result_count = len(response.data['results'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        count = Services.objects.filter(profile=profile).count()

        if count < 10:
            self.assertEqual(result_count, count)
        else:
            self.assertLessEqual(result_count, 10)


    def tearDown(self):
        print('[INFO] End test\n')