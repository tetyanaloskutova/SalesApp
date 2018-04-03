from django.test import TestCase

from .models import RiskField, RiskType
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from salesaccounts.views import RiskTypeViewSet, RiskFieldViewSet

class RiskModelTestCase(TestCase):
	"""This class defines the test suite for the RiskType/RiskField model."""

	def setUp(self):
		self.defaultUser = User.objects.create_user(username='testuser', password='12345678')
		
		self.risktype1 = RiskType.objects.create(user_risktype = self.defaultUser, name="Address", description = "Property address")
		self.risktype1.save()
		self.risktype2 = RiskType.objects.create(user_risktype = self.defaultUser, name="Model", description="Car model")
		self.risktype2.save()
		
	def test_model_can_create_a_RiskField(self):
		"""Test the RiskField model can create a RiskField."""
		RiskField.objects.create(user_riskfield = self.defaultUser, risktype = self.risktype2, name="field", description="field")
		self.assertEqual(RiskField.objects.count(), 1)

		
	def test_model_can_select_a_RiskField(self):
		"""Test the RiskField model can select a RiskField."""
		riskfield = RiskField.objects.create(user_riskfield = self.defaultUser, risktype = self.risktype1, name="field", description="field")
		riskfield.save()
		riskfield_retrieved = RiskField.objects.get(risktype = self.risktype1)
		self.assertEqual(riskfield, riskfield_retrieved)
		

		
	def test_model_can_create_a_RiskType(self):
		"""Test the RiskType model can create a RiskType."""
		old_count = RiskType.objects.count()
		risktype = RiskType(user_risktype = self.defaultUser, name="Test risk type", description="Test risk type")
		risktype.save()
		new_count = RiskType.objects.count()
		self.assertNotEqual(old_count, new_count)
		
	def test_select_risktype(self):
		"""Test the RiskType model can select a RiskType."""
		risktype = RiskType(user_risktype = self.defaultUser, name="Test risk type", description="Test risk type")
		risktype.save()
		risktype_retrieved = RiskType.objects.get(name="Test risk type", description="Test risk type")
		self.assertEqual(risktype, risktype_retrieved)
		

		
class RiskTypeViewsTests(APITestCase):
	"""This class defines the test suite for the RiskType views."""
	def setUp(self):
		self.defaultUser = User.objects.create_superuser(username='testuser', email = 'd@d.com', password='12345678')
		
	def test_view_set(self):
		"""Test the RiskType view can retrieve a RiskType."""
		request = APIRequestFactory().get("")
		user = User.objects.get(username='testuser')
		force_authenticate(request, user=user)
		risktype_detail = RiskTypeViewSet.as_view({'get': 'retrieve'})
		risktype = RiskType.objects.create(user_risktype = self.defaultUser, name="Test risk type", description="Test risk type")
		response = risktype_detail(request, pk=risktype.pk)
		self.assertEqual(response.status_code, 200)   
		self.assertEqual(response.data['name'], risktype.name)        
		self.assertEqual(response.data['description'], risktype.description)        
		
	
	def test_list_risktype_empty(self):
		"""Test the RiskType view can retrieve an empty list."""
		request = APIRequestFactory().get("")
		risktype_list = RiskTypeViewSet.as_view({'get': 'list'})
		response = risktype_list(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 0)

	def test_list_risktype(self):
		"""Test the RiskType view can retrieve Risktype list."""
		request = APIRequestFactory().get("")
		user = User.objects.get(username='testuser')
		force_authenticate(request, user=user)
		RiskType.objects.create(user_risktype = self.defaultUser, name="Test risk type 1", description="Test risk type")
		RiskType.objects.create(user_risktype = self.defaultUser, name="Test risk type 2", description="Test risk type")
		
		risktype_list = RiskTypeViewSet.as_view({'get': 'list'})
		response = risktype_list(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 2)
	
		
class RiskFieldViewsTests(APITestCase):
	"""This class defines the test suite for the RiskField views."""
	def setUp(self):
		self.defaultUser = User.objects.create_superuser(username='testuser', email = 'd@d.com', password='12345678')
		
	def test_view_set(self):
		"""Test the RiskField view can retrieve a RiskField."""
		request = APIRequestFactory().get("")
		user = User.objects.get(username='testuser')
		risktype = RiskType.objects.create(user_risktype = self.defaultUser, name="Address", description = "Property address")
		force_authenticate(request, user=user)
		riskfield_detail = RiskFieldViewSet.as_view({'get': 'retrieve'})
		riskfield = RiskField.objects.create(user_riskfield = self.defaultUser, risktype = risktype,
			name="Test risk field", description="Test risk field")
		response = riskfield_detail(request, pk=riskfield.pk)
		self.assertEqual(response.status_code, 200)        
		self.assertEqual(response.data['name'], riskfield.name)        
		self.assertEqual(response.data['order'], riskfield.order)        
		
	
	def test_list_riskfield_empty(self):
		"""Test the RiskField view can retrieve an empty list."""
		request = APIRequestFactory().get("")
		user = User.objects.get(username='testuser')
		force_authenticate(request, user=user)
		
		riskfield_list = RiskFieldViewSet.as_view({'get': 'list'})
		response = riskfield_list(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 0)

	
	def test_list_riskfield(self):
		"""Test the RiskField view can retrieve all RiskFields."""
		request = APIRequestFactory().get("")
		user = User.objects.get(username='testuser')
		force_authenticate(request, user=user)
		risktype = RiskType.objects.create(user_risktype = self.defaultUser, name="Address", description = "Property address")
		
		riskfield_detail = RiskFieldViewSet.as_view({'get': 'retrieve'})
		riskfield = RiskField.objects.create(user_riskfield = self.defaultUser, risktype = risktype,
			name="Test risk field", description="Test risk field")
		
		riskfield_list = RiskFieldViewSet.as_view({'get': 'list'})
		response = riskfield_list(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 1)
	