from django.test import TestCase

from .models import RiskField, RiskType, RiskTypeFieldMap
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

class RiskModelTestCase(TestCase):
	"""This class defines the test suite for the RiskType model."""

	def setUp(self):
		users = User.objects.all()
		for u in users:
			print(u)
		#self.user = User.objects.get(username='amin')
		RiskType.objects.create(name="Address", description = "Property address")
		RiskType.objects.create(name="Model", description="Car model")
		self.assertEqual(RiskType.objects.count(), 2)

	def test_model_can_create_a_RiskType(self):
		"""Test the RiskType model can create a RiskType."""
		old_count = RiskType.objects.count()
		risktype = RiskType(name="Test risk type", description="Test risk type")
		risktype.save()
		new_count = RiskType.objects.count()
		self.assertNotEqual(old_count, new_count)
		
	def test_select_risktype(self):
		risktype = RiskType(name="Test risk type", description="Test risk type")
		risktype.save()
		risktype_retrieved = RiskType.objects.get(name="Test risk type", description="Test risk type")
		self.assertEqual(risktype, risktype_retrieved)
		
		
class ViewTestCase(TestCase):
	"""Test suite for the risktypes views."""

	def setUp(self):
		"""Define the test client and other test variables."""
		self.client = APIClient()
		self.risktype_data = {'name': 'Test risk type', 'description': 'Test risk type','organization': 'Test org'}
		self.response = self.client.post(
			reverse('create'),
			self.risktype_data,
			format="json")

	def test_api_can_create_a_risktype(self):
		"""Test the api has risktype creation capability."""
		self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)		
		
		
	def test_api_can_get_a_risktype(self):
        """Test the api can get a given risktype."""
        risktype = RiskType.objects.get()
        response = self.client.get(
            reverse('details',
            kwargs={'pk': risktype.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, risktype)

    def test_api_can_update_risktype(self):
        """Test the api can update a given risktype. This is concerned with marking Risk types as deleted """
        change_risktype = {'deleted_date': timezone.now}
        res = self.client.put(
            reverse('details', kwargs={'pk': risktype.id}),
            change_risktype, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
