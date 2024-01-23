from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import *


class GetDataTestCase(APITestCase):
    fixtures = ['comp_service_brands.json',
                'comp_service_devices.json',
                'comp_service_managers.json',
                'comp_service_owners.json',
                'comp_service_models.json',
                'comp_service_services.json',
                'comp_service_specialists.json']

    
    def setUp(self):
        print('[INFO] Start get test')


    def check_read_all(self, url_name: str) -> None:
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 10)


    def test_get_all_specialists(self):
        self.check_read_all('specialists-all')


    def test_get_all_services(self):
        self.check_read_all('services-all')
        

    def test_get_all_devices(self):
        self.check_read_all('devices-all')


    def test_get_all_requests(self):
        self.check_read_all('requests-all')


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
        print('[INFO] End get test\n')



class AddDataTests(APITestCase):
    fixtures = ['comp_service_managers.json',
                'comp_service_owners.json',
                'comp_service_models.json',
                'comp_service_brands.json',
                'comp_service_services.json',
                'comp_service_specialists.json']
    

    def setUp(self):
        print('[INFO] Start add test')


    def test_create_request(self):
        url = reverse('create-request')
        data = {
            'manager': 1,
            'client': 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Requests.objects.count(), 1)


    def test_create_device(self):
        url = reverse('create-device')
        data = {
            "type": "laptop",
            "model": 2,
            "year": 2019,
            "owner": 2,
            "specialists": [3, 6],
            "services": [7, 9, 14]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Devices.objects.count(), 1)


    def tearDown(self):
        print('[INFO] End add test\n')



class UpdateDataTests(APITestCase):
    fixtures = ['comp_service_owners.json',
                'comp_service_models.json',
                'comp_service_brands.json',
                'comp_service_services.json',
                'comp_service_specialists.json']

    def setUp(self):
        print('[INFO] Start update test')


    def test_update_device_status(self):
        pk = 1
        url = reverse('update-device', args=(pk,))
        data = {
            'status': 1
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def tearDown(self):
        print('[INFO] End update test\n')