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


    def check_read_all(self, url_name: str,
                       status_: int = status.HTTP_200_OK) -> None:
        url = reverse(url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_)
        if status_ == status.HTTP_200_OK:
            self.assertLessEqual(len(response.data['results']), 10)


    def test_get_all_specialists(self):
        self.check_read_all('specialists-all')


    def test_get_all_services(self):
        self.check_read_all('services-all')
        

    def test_get_all_devices(self):
        self.check_read_all('devices-all', status_=status.HTTP_403_FORBIDDEN)


    def test_get_all_requests(self):
        self.check_read_all('requests-all', status_=status.HTTP_403_FORBIDDEN)


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
                'comp_service_devices.json',
                'comp_service_owners.json',
                'comp_service_models.json',
                'comp_service_brands.json',
                'comp_service_services.json',
                'comp_service_specialists.json',
                'auth_user.json']
    

    def setUp(self):
        url_login = '/auth/token/login/'
        response = self.client.post(url_login,
                                    data={"username": "root",
                                          "password": "qwerty12!"})
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        print('[INFO] Start add test')


    def test_create_client_and_request(self):
        url = reverse('create-client')
        data = {
            "name": "Marik",
            "phone_number": "6723573214",
            "email": 'example@mail.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_request(self):
        url = reverse('create-request')
        data = {
            'manager': 1,
            'client': 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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


    def tearDown(self):
        url_logout = '/auth/token/logout/'
        self.client.post(url_logout)
        print('[INFO] End add test\n')



class UpdateDataTests(APITestCase):
    fixtures = ['comp_service_owners.json',
                'comp_service_devices.json',
                'comp_service_requests.json',
                'comp_service_managers.json',
                'comp_service_models.json',
                'comp_service_brands.json',
                'comp_service_services.json',
                'comp_service_specialists.json',
                'auth_user.json']


    def setUp(self):
        url_login = '/auth/token/login/'
        response = self.client.post(url_login,
                                    data={"username": "root",
                                          "password": "qwerty12!"})
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        print('[INFO] Start update test')


    def test_update_request_manager(self):
        pk = 3
        url = reverse('request', args=(pk,))
        data = {'manager': 2}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_device_status(self):
        pk = 2
        url = reverse('update-device', args=(pk,))
        data = {'status': 1}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def tearDown(self):
        url_logout = '/auth/token/logout/'
        self.client.post(url_logout)
        print('[INFO] End update test\n')



class DeleteDataTests(APITestCase):
    fixtures = ['comp_service_requests.json',
                'comp_service_managers.json',
                'comp_service_owners.json',
                'auth_user.json']
    

    def setUp(self):
        url_login = '/auth/token/login/'
        response = self.client.post(url_login,
                                    data={"username": "root",
                                          "password": "qwerty12!"})
        print(response.data)
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        print('[INFO] Start delete test')
    

    def test_delete_request(self):
        pk = 1
        url = reverse('delete-request', args=(pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def tearDown(self):
        url_logout = '/auth/token/logout/'
        self.client.post(url_logout)
        print('[INFO] End delete test\n')