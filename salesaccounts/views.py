from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
import openpyxl
import os
from django.utils import timezone
	
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

@login_required
@api_view(['GET',])
def import_services(request):

	df_service_types = pd.read_excel('data/SL - lookup table.xlsx')
	df_groups = df_service_types.groupby(['Group', 'Name']).size().reset_index().rename(columns={0:'Count'})	
	
	for index, row in df_groups.iterrows():
		try:
			service = models.ServiceType.objects.get(service_type = row[0], service_name = row[1])
		except:
			service = models.ServiceType()
			service.service_type = row[0]
			service.service_name = row[1]
			service.user_account = request.user
			service.save()
				
		
	for index, row in df_service_types.iterrows():
		try:
			sales_lead = models.SalesLead.objects.get(CRM_id = row[0])
			try:
				service = models.ServiceType.objects.get(service_type = row[1], service_name = row[2])
				sales_lead.service_type = service
				sales_lead.save()
			except:
				pass
		except:
			pass
	
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
	
@login_required
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
				lead.created_on = timezone.now()
				
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
			lead.probability = row['Probability_Tool']
			
		try:
			lead.actual_close_date = datetime.strptime(row['Actual Close Date'], '%d/%m/%Y  %H:%M')
		except:
			lead.actual_close_date = None
		  
		lead.sales_originator = models.CREmployee.objects.get(name = row['Sales Originator'])
		lead.service_group = row['Service Group']
		lead.contact = row['Contact']
		lead.country = row['Country']
		lead.est_revenue_USD =  float(str(row['Est. Revenue (USD)']).replace(',' , ''))
		try:
			lead.est_decision_date = datetime.strptime(row['Est. Decision Date'], '%d/%m/%Y')
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
	
def export_leads_function():
	leads = models.SalesLead.objects.all().prefetch_related('account', 'service_type')

	df = pd.concat([pd.DataFrame([[lead.status, lead.account.name 
		,lead.sales_originator.name if lead.sales_originator else 'N/A', lead.service_group, lead.CRM_id
		,lead.created_on, lead.name, lead.contact,lead.country, lead.est_revenue_USD
		, lead.est_decision_date, lead.owner.name if lead.owner else 'N/A'
		, lead.pm.name if lead.pm else 'N/A', lead.probability, lead.next_action, lead.next_action_description
		, lead.next_action_date, str(lead.next_action_person) if lead.next_action_person else 'N/A'
		, lead.service_type.service_type if lead.service_type else 'N/A'
		,lead.service_type.service_name if lead.service_type else 'N/A'
		, lead.actual_close_date
		, lead.account.is_top40]], columns=['Status','Account','Sales Originator','Service Group'
		,'Reference #','Created On','Name', 'Contact', 'Country', 'Est. Revenue (USD)'
		, 'Est. Decision Date', 'Sales Lead Owner'
		, 'Full Name (Service Line PM)', 'Probability_Tool', 'Next action', 'Next action description'
		,'Next action date', 'Next action persion', 'Service line', 'Service line department', 'Actual Close Date', 'Is top 40' ]
		) for lead in leads],
		ignore_index=True)
	
	writer = pd.ExcelWriter('data/CRM_leads_export.xlsx')
	df.to_excel(writer, index=False)
	writer.save()
	
@login_required
@api_view(['GET',])		
def export_leads(request):	
		
	"""
	df1 = pd.DataFrame.from_records(models.SalesLead.objects.all().prefetch_related('account', 'service_type').values('service_type.service_type'))
	
	df = pd.DataFrame(columns=['Status','Account','Sales Originator','Service Group'
		,'Reference #','Created On','Name', 'Contact', 'Country', 'Est. Revenue (USD)'
		, 'Est. Decision Date', 'Sales Lead Owner', 'Sales Lead Title'
		, 'Full Name (Service Line PM)', 'Full Name (Owning User)', 'Probability_Tool', 'Next action'
		, 'Next action description','Next action date', 'Next action persion', 'Service line', 'Service line department' ])
	"""
		
	"""	
	return Response(['{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}'.format(lead.status, lead.account.name 
		,lead.sales_originator, lead.service_group, lead.CRM_id
		,lead.created_on, lead.name, lead.contact, lead.est_revenue_USD
		, lead.est_decision_date, lead.owner, lead.name
		, lead.pm, lead.probability, lead.next_action, lead.next_action_description
		, lead.next_action_date, lead.next_action_person, lead.service_type.service_type
		,lead.service_type.service_name)  for lead in leads])
	"""
	try :
		export_leads_function()
		return Response('Export successful')
	except Exception as e:
		return Response('Export unsuccessful, error {0}'.format(str(e)))
	
	
@login_required
@api_view(['GET',])		
def get_current_directory(request):
	return Response(os.getcwd())
	