from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from .models import Location, Boundary
from django.contrib.gis.geos import Point, Polygon


class UserTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_user(self):
        url = '/register/'
        data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': '1234'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login_user(self):
        url = '/register/'
        data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': '1234'
        }
        self.client.post(url, data)

        url = '/login/'
        data = {
            'username': 'testuser',
            'password': '1234'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.json())


class LocationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.login(username='testuser', password='1234')

    def test_create_location(self):
        url = '/api/locations/'
        data = {
		    "name": "Test Location",
		    "description": "Test location description",
		    "coordinates": {
		        "type": "Point",
		        "coordinates": [-73.9712, 40.7831]
		    }
		}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(Location.objects.get().name, 'Test Location')

    def test_get_location_list(self):
        Location.objects.create(name='Test Location', description='A test location', coordinates=Point(-73.9712, 40.7831))
        url = '/api/locations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_update_location(self):
        location = Location.objects.create(name='Test Location', description='A test location', coordinates=Point(-73.9712, 40.7831))
        url = f'/api/locations/{location.id}/'
        data = {'name': 'Updated Location'}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.get().name, 'Updated Location')

    def test_delete_location(self):
        location = Location.objects.create(name='Test Location', description='A test location', coordinates=Point(-73.9712, 40.7831))
        url = f'/api/locations/{location.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0)


class BoundaryTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.login(username='testuser', password='1234')

        self.coordinates = [
		            [
		                [78.030155, 27.180015],
		                [78.030155, 27.170015],
		                [78.050155, 27.170015],
		                [78.050155, 27.180015],
		                [78.030155, 27.180015]
		            ]
		        ]

    def test_create_boundary(self):
        url = '/api/boundaries/'
        data = {
            'name': 'Test Boundary',
            'area': {
		        "type": "Polygon",
		        "coordinates": self.coordinates
		    }
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Boundary.objects.count(), 1)
        self.assertEqual(Boundary.objects.get().name, 'Test Boundary')

    def test_get_boundary_list(self):
        Boundary.objects.create(name='Test Boundary', area=Polygon(self.coordinates[0]))
        url = '/api/boundaries/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_update_boundary(self):
        boundary = Boundary.objects.create(name='Test Boundary', area=Polygon(self.coordinates[0]))
        url = f'/api/boundaries/{boundary.id}/'
        data = {'name': 'Updated Boundary'}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Boundary.objects.get().name, 'Updated Boundary')

    def test_delete_boundary(self):
        boundary = Boundary.objects.create(name='Test Boundary', area=Polygon(self.coordinates[0]))
        url = f'/api/boundaries/{boundary.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Boundary.objects.count(), 0)


class CalculateDistanceTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.login(username='testuser', password='1234')

    def test_calculate_distance(self):
        location1 = Location.objects.create(name='Location 1', description='First location', coordinates=Point(78.042155, 27.175015))
        location2 = Location.objects.create(name='Location 2', description='Second location', coordinates=Point(77.185455, 28.524428))
        url = '/api/locations/distance/'
        data = {
            'location1_id': location1.id,
            'location2_id': location2.id
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['distance'], 1.5983899194404934)


class CheckBoundaryTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.login(username='testuser', password='1234')
        self.coordinates = [
			            [
			                [78.030155, 27.180015],
			                [78.030155, 27.170015],
			                [78.050155, 27.170015],
			                [78.050155, 27.180015],
			                [78.030155, 27.180015]
			            ]
			        ]

    def test_check_boundary(self):
        location1 = Location.objects.create(name='Location 1', description='First location', coordinates=Point(77.185455, 28.524428))
        location2 = Location.objects.create(name='Location 2', description='Second location', coordinates=Point(78.0421, 27.1751))
        boundary = Boundary.objects.create(name='Test Boundary', area=Polygon(self.coordinates[0]))
        url = '/api/locations/within_boundary/'
        data1 = {
            'location_id': location1.id,
            'boundary_id': boundary.id
        }
        data2 = {
            'location_id': location2.id,
            'boundary_id': boundary.id
        }
        response1 = self.client.post(url, data1, content_type='application/json')
        response2 = self.client.post(url, data2, content_type='application/json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertFalse(response1.json()['is_within'])
        self.assertTrue(response2.json()['is_within'])
