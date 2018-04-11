from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .serializers import *
from .permissions import IsStaffOrOwner, IsStaffOrOwnerField
from salesaccounts import models
from rest_framework import generics
from django.shortcuts import render
from django.forms.models import model_to_dict
import csv
from rest_framework.decorators import api_view
from datetime import datetime

	
class AccountViewSet(viewsets.ModelViewSet):
	serializer_class = AccountSerializer
	permission_classes = (IsStaffOrOwnerField,)

	def get_queryset(self):
		if self.request.user.is_superuser:
			return models.Account.objects.all()
		else:
			return models.Account.objects.filter(user_riskfield=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user_riskfield=self.request.user)

class PersonViewSet(viewsets.ModelViewSet):
	serializer_class = PersonSerializer
	permission_classes = (IsStaffOrOwner,)

	def get_queryset(self):
		if self.request.user.is_superuser:
			return models.Person.objects.all()
		else:
			return models.Person.objects.all() #filter(user_risktype = self.request.user)

	def perform_create(self, serializer):
		serializer.save(user_risktype = self.request.user)

	# The detail_route allows me to see all the riskfields of a risk type
	# with the following URL: /salesaccounts/risktype/(?P<pk>\d+)/riskfields
"""
	@detail_route(url_path='formatted')
	def account_persons (self, request, pk):
		account = models.Account.objects.get(pk=pk)
		riskfields = risktype.risktype_riskfield.all().order_by('order')
		serializer = RiskFieldSerializer(riskfields, context={'request': request})
		return Response([riskfield.name for riskfield in riskfields])
"""

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
"""	
def index(request, pk):
	risktype = models.RiskType.objects.get(pk=pk)
	riskfields = risktype.risktype_riskfield.all().order_by('order')
			
	context_fields = []	
	for riskfield in riskfields:
		context_fields.append(model_to_dict(riskfield, fields=['id','name', 'type','length','enum_values']))
		
	context = {}
	context['title'] = risktype.name
	context['fields'] = context_fields
	

	return render(request, 'risktype.html', context)	
"""	

@api_view(['GET',])
def import_services(request):

	serviceTypes = models.ServiceType.objects.all()
	if (len(serviceTypes)>0):
		return Response('serviceTypes not empty')
	dataReader = csv.reader(open('service.csv'), delimiter=',') 
	for row in dataReader: 
		serviceType = models.ServiceType() 
		serviceType.user_account = request.user
		serviceType.service_type = row[0] 
		serviceType.service_name = row[1] 
		serviceType.save()
		
	serviceTypes = models.ServiceType.objects.all()
	return Response([serviceType.service_name for serviceType in serviceTypes])
		
	
@api_view(['GET',])
def import_accounts(request):

	accounts = models.Account.objects.all()
	if (len(accounts)>0):
		return Response('accounts not empty')
		
	dataReader = csv.reader(open('accounts.csv'), delimiter=',') 
	for row in dataReader: 
		account = models.Account() 
		account.user_account = request.user
		account.name = row[0]
		try:
			account.account_manager = models.CREmployee.objects.get(short_name = row[1])
		except:
			account.account_manager = None
			
		 
		account.sector = row[2] 
		account.relationship_status = row[3]
		account.region = row[4]
		account.save()
		
	account = models.Account()
	account.name = 'Undefined'
	account.user_account = request.user
	account.sector = 'Undefined'
	account.relationship_status = 'Undefined'
	account.region = 'Undefined'
	account.save()
		
	accounts = models.Account.objects.all()
	return Response([account.name for account in accounts])
	

@api_view(['GET',])
def import_cremployee(request):

	employees = models.CREmployee.objects.all()
	if (len(employees)>0):
		return Response('employees not empty')
		
	dataReader = csv.reader(open('cremployees.csv'), delimiter=',') 
	for row in dataReader: 
		employee = models.CREmployee() 
		employee.user_account = request.user
		employee.short_name = row[0] 
		employee.name = row[1] 
		
		employee.save()
		
	employees = models.CREmployee.objects.all()
	return Response([employee.name for employee in employees])
		
@api_view(['GET',])		
def import_leads(request):
	leads = models.SalesLead.objects.all()
	if (len(leads)>0):
		return Response('leads not empty')
		
	dataReader = csv.reader(open('Leads.csv'), delimiter=';') 
	for row in dataReader: 
		lead = models.SalesLead() 
		lead.user_account = request.user
		lead.status = row[0]
		try:
			lead.account = models.Account.objects.get(name = row[1])
		except:
			lead.account = models.Account.objects.get(name = 'Undefined')
			
		lead.country	= row[2]
		
		try:
			lead.owner = models.CREmployee.objects.get(name = row[3])
		except:
			lead.owner = None
		
		try:
			lead.service_type = models.ServiceType.objects.get(service_name = row[4])
		except:
			lead.service_type = None
		
		lead.CRM_id =  row[5]
		if len(row[6])> 0:
			lead.created_on = datetime.strptime(row[6], '%d/%m/%Y')
		else:
			lead.created_on = None
		if len(row[7])> 0:
			lead.est_decision_dat = datetime.strptime(row[7], '%d/%m/%Y')
		else:
			lead.est_decision_dat = None
		lead.Probability = row[8]	
		lead.contact = row[9]
		lead.status_reason = row[10] 
		if len(row[11])> 0:
			lead.actual_close_date = datetime.strptime(row[11], '%d/%m/%Y')
		else:
			lead.actual_close_date = None
			
		lead.est_revenue_GBP	= row[12]
		lead.description	= row[13]
		lead.sales_narrative = row[14]
		
		lead.save()
		
	leads = models.SalesLead.objects.all()
	return Response([lead.name for lead in leads])
		