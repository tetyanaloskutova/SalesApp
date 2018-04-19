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
import pandas as pd
import string
	
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

	df_services = pd.read_excel('data/SL - lookup table.xlsx')	
	
	df_accounts = df_accounts[df_accounts['Top 40?'] == 'Y']
	for index, row in df_accounts.iterrows():
		try:
			account = models.Account.objects.get(name = row[0])
			account.is_top40 = True
			account.save()
		except:
			account = None
			
		
		
	serviceTypes = models.ServiceType.objects.all()
	return Response([serviceType.service_name for serviceType in serviceTypes])
		
	
@api_view(['GET',])
def import_accounts(request):

	"""accounts = models.Account.objects.all()
	for account in accounts:
		account.is_top40 = False 
		account.save()
	"""
	df_accounts = pd.read_excel('data/TOP40_load.xlsx')	
	
	df_accounts = df_accounts[df_accounts['Top 40?'] == 'Y']
	for index, row in df_accounts.iterrows():
		try:
			account = models.Account.objects.get(name = row[0])
			account.is_top40 = True
			account.save()
		except:
			account = None
			
		
		
	accounts = models.Account.objects.all()	
	return Response([(account.name + ':' + str(account.is_top40)) for account in accounts])
	
"""
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
"""

def import_cremployees(df_leads, request):
	translator = str.maketrans('', '', string.ascii_lowercase)
	
	pm_list = df_leads['Full Name (Service Line PM)']
	originator_list = df_leads['Sales Originator']
	owners_list = df_leads['Full Name (Owning User)']
	
	pm_set = set(pm_list.tolist())
	originator_set = set(originator_list.tolist())
	owners_set = set(owners_list.tolist())
	
	unique_set =  set(list(pm_set) + list(owners_set) + list(originator_set))
	
	for id in set(unique_set):
		try:
			employee = models.CREmployee.objects.get(name = id)
		except:
			employee = models.CREmployee()
			employee.name = id
			employee.user_account = request.user
			#employee.short_name = id.translate(translator)
			employee.save()
	
	
@api_view(['GET',])		
def import_leads(request):
	"""'Status', 'Account', 'Countries',
       'Sales Originator', 'Service Group', 'Reference #', 'Created On',
       'Name', 'Contact', 'Country', 'Est. Revenue (USD)',
       'Est. Decision Date', 'Sales Lead Owner', 'Sales Lead Title',
       'Sales Lead', 'Full Name (Service Line PM)',
       'Full Name (Owning User)'  """
	   
	df_leads = pd.read_excel('data/CRM_leads.xlsx')	
	
	import_cremployees(df_leads, request)
	
	# If SL does not exists - create, otherwise - update
	for index, row in df_leads.iterrows():
		lead = None 
		try:
			lead = models.SalesLead.objects.get(CRM_id = row["Reference #"])		
		except:
			lead = models.SalesLead()
			lead.status = row['Status']
			lead.CRM_id = row['Reference #']
			try:
				lead.created_on = datetime.strptime(row['Created On'], '%d/%m/%Y  %H:%M')
			except:
				lead.created_on = timezone.now
				
			try:
				lead.account = models.Account.objects.get(name = row['Account'])
			except:
				account = models.Account()
				account.name = row['Account']
				account.region = row['Country']
				account.account_manager = models.CREmployee.objects.get(name = row['Full Name (Owning User)'])
				account.user_account = request.user
				account.save()
				lead.account = account
				
			lead.name = row['Name']
			
		
		
		lead.sales_originator = models.CREmployee.objects.get(name = row['Sales Originator'])
		lead.service_group = row['Service Group']
		lead.contact = row['Contact']
		lead.country = row['Country']
		lead.est_revenue_USD =  float(str(row['Est. Revenue (USD)']).replace(',' , ''))
		try:
			lead.est_decision_date = datetime.strptime(row['Est. Decision Date'], '%d/%m/%Y  %H:%M')
		except:
			lead.est_decision_date = None
		lead.owner = models.CREmployee.objects.get(name = row['Sales Lead Owner'])
		lead.pm = models.CREmployee.objects.get(name = row['Full Name (Service Line PM)'])
		lead.owning_user = models.CREmployee.objects.get(name = row['Full Name (Owning User)'])
		
		lead.user_account = request.user
			
			
		try:
			lead.service_type = models.ServiceType.objects.get(service_name = row[4])
		except:
			lead.service_type = None
		
		lead.save()
		
	leads = models.SalesLead.objects.all()
	return Response([lead.name for lead in leads])
		