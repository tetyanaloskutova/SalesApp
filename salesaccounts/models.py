import locale
	
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

"""
TO DO: change models.CASCADE to models.SET_NULL
"""
class CREmployee(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
		
	name = models.CharField(max_length=256)
	short_name = models.CharField(max_length=256)
	
	
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max, editable = False)
	history = HistoricalRecords()
		
	def __str__(self):
		return '{0}'.format(self.name)
		
	
	class Meta:
		verbose_name = 'CR Employee'
		verbose_name_plural = 'CR Employees'	

class AccountGroup(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False, blank = True)
	name = models.CharField(max_length=256)
	
	history = HistoricalRecords()
	
	def __str__(self):
		return '{0}'.format(self.name)
	
	
class Account(models.Model):
	# 'Key Account', 'Sector', 'Relationship status', 'Region', 'Account Manager'
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	account_group = models.ForeignKey(AccountGroup, related_name="+", null = True, on_delete = models.SET_NULL,)
	
	name = models.CharField(max_length=256)
	is_executive = models.BooleanField(verbose_name='Executive', default = False)
	is_management = models.BooleanField(verbose_name='Management', default = False)
	is_user = models.BooleanField(verbose_name='User', default = False)
	
	sector = models.CharField(max_length=256, null = True)
	
	SUPER = '3'
	GOOD = '2'
	AVERAGE = '1'
	COLD = '0'
	
	TYPE_CHOICES = (
		(SUPER, 'Super'),
		(GOOD, 'Good'),
		(AVERAGE, 'Okay'),	
		(COLD, 'Worrying'),	
	)
	relationship_status = models.CharField(max_length=256,choices=TYPE_CHOICES,
		default=COLD)
	
	region = models.CharField(max_length=256, null = True)
	account_manager = models.ForeignKey(CREmployee, related_name="+", null = True, on_delete = models.SET_NULL,)
	
	is_top40 = models.BooleanField(verbose_name = 'Top 40 Account', default = False)
	
	date_created = models.DateTimeField(default=timezone.now, editable= False)
	
	
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	date_deleted = models.DateTimeField(default=timezone.datetime.max, editable= False)
	
	history = HistoricalRecords()
	
	def __str__(self):
		if (self.account_group):
			return '{0}: {1}'.format(self.account_group, self.name)
		else:
			rel = ''
			if self.relationship_status == '1':
				rel = 'Okay relationship' 
			else:
				if self.relationship_status == '2':
					rel = 'Good relationship'
				else:
					if self.relationship_status == '3':
						rel = 'Excellent relationship'
					else:
						rel = 'No relationship status'
					
			return '{0}: {1}'.format(self.name, rel)	
	
	
	class Meta:
		verbose_name = 'Account'
		verbose_name_plural = 'Accounts'



class Person(models.Model):
	
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	lastname = models.CharField(max_length=256)
	firstname = models.CharField(max_length=256)
	
	
	date_created = models.DateTimeField(default=timezone.now)
	history = HistoricalRecords()
	
	class Meta:
		verbose_name = 'Person'
		verbose_name_plural = 'Persons'


class AccountPerson(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	accountperson_person = models.ForeignKey(Person, related_name="+", on_delete = models.CASCADE,)
	accountperson_account = models.ForeignKey(Account, related_name="+", on_delete = models.CASCADE,)
	
	date_created = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)
	
	

class ServiceType(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	service_type = models.CharField(max_length=256)
	service_name = models.TextField(default = '')
	history = HistoricalRecords()
			
			
	def __str__(self):
		return '{0}: {1}'.format(self.service_type, self.service_name)
	
			
		
class SalesLead(models.Model):
	""" 'Status', 'Account', 'Countries',
       'Sales Originator', 'Service Group', 'Reference #', 'Created On',
       'Name', 'Contact', 'Country', 'Est. Revenue (USD)',
       'Est. Decision Date', 'Sales Lead Owner', 'Sales Lead Title',
       'Sales Lead', 'Full Name (Service Line PM)', 'Name (Originating Lead)',
       'Full Name (Owning User)'  """
	#locale.setlocale( locale.LC_ALL, 'english_USA' ) 
	
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	# Status	Account	Country	Owner	Service Group	Reference #	Created On	Est. Decision Date	Probability	Contact	Status Reason	Actual Close Date	Est. Revenue (GBP)	Description	Proposal	Saales Narrative
	
	OPEN = '1'
	WON = '2'
	LOST = '3'
	
	TYPE_CHOICES = (
		(OPEN, 'Open'),
		(WON, 'Won'),
		(LOST, 'Lost'),	
	)
	status = models.CharField(max_length=256,choices=TYPE_CHOICES,
		default=OPEN)
		
	account = models.ForeignKey(Account, related_name="+", null=True, on_delete = models.SET_NULL, blank = True)
	country	= models.CharField(max_length=256)
	sales_originator = models.ForeignKey(CREmployee, related_name="+", null=True, on_delete = models.SET_NULL,)		
	service_group = models.CharField(max_length=256, null=True, blank = True)	
	owner = models.ForeignKey(CREmployee, related_name="+", null=True, on_delete = models.SET_NULL,)	
	service_type = models.ForeignKey(ServiceType, related_name="+", null=True, on_delete = models.SET_NULL,)
	competitors = models.CharField(max_length=256, null=True, blank = True)	
	partners = models.CharField(max_length=256, null=True, blank = True)	
	
	CRM_id =  models.CharField(max_length=256, null=True, blank = True)	
	created_on = models.DateTimeField(default=timezone.now, null=True, editable=False)	
	created_on_date = models.DateField(default=timezone.now, null=True, editable=False)	
	name = models.CharField(max_length=256)
	est_decision_date = models.DateField(verbose_name = 'Estimated close date', default=timezone.now, null=True, blank = True)
	
	probability	= models.IntegerField(default=50,
		validators=[
			MaxValueValidator(100),
			MinValueValidator(0)
		])
	contact	= models.CharField(max_length=256, null = True, blank = True)
	status_reason = models.CharField(max_length=256, blank = True)
	actual_close_date = models.DateField(default=timezone.now, null=True, blank = True)
	actual_close_time = models.DateTimeField(default=timezone.now, null=True, editable=False)
	est_revenue_USD	= models.FloatField(default = 0, null = True)
	pm = models.ForeignKey( CREmployee, related_name="+", null=True, on_delete = models.SET_NULL,verbose_name = 'Project Manager',)		
	owning_user = models.ForeignKey(CREmployee, related_name="+", null=True, on_delete = models.SET_NULL,)		
	
	description	= models.TextField(default = r'''Product:-
Competition:-
Partners:-
Compelling reason:-
Next steps:-
''', null=True, blank = True)
	
	next_action = models.TextField(default = '', null=True, blank = True)
	next_action_date = models.DateField(default=None, null=True, blank = True)
	next_action_description = models.TextField(default = '', null=True, blank = True)
	next_action_person = models.ForeignKey(CREmployee, related_name="+", null=True, on_delete = models.SET_NULL,)		
	
	history = HistoricalRecords()

	
	def __str__(self):
		return '{0}: ({1})'.format(self.name, self.status)
	
		
	class Meta:
		verbose_name = 'Sales Lead'
		verbose_name_plural = 'Sales Leads'

		
class Project(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	date_created = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)

	
		

class Schedule(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	scheduled = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)

		
		

class Meeting(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	meeting_schedule = models.ForeignKey(Schedule, related_name="+", on_delete = models.CASCADE,)
	
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	meeting_schedule = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)

	class Meta:
		verbose_name = 'Meeting'
		verbose_name_plural = 'Meetings'
	


class MeetingMinutes(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	
	meetingminutes_meeting = models.ForeignKey(Meeting, related_name="+", on_delete = models.CASCADE,)
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	meeting_schedule = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)

	class Meta:
		verbose_name = 'MeetingMinutes'
		verbose_name_plural = 'MeetingMinutes'

		
class ScheduledEmployee(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	scheduledemployee_schedule = models.ForeignKey(Schedule, related_name="+", on_delete = models.CASCADE,)
	
	
	name = models.CharField(max_length=256)
	description = models.TextField(default = '')
	meeting_schedule = models.DateTimeField(default=timezone.now)
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)
	
	
	
class Attachment(models.Model):
	user_account = models.ForeignKey(User, related_name="+", on_delete = models.CASCADE, editable=False)
	attachment_meeting = models.ForeignKey(Meeting, related_name="+", on_delete = models.CASCADE,)
	
	
	name = models.CharField(max_length=256)
	path = models.TextField(default = '')
	timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
	
	date_deleted = models.DateTimeField(default=timezone.datetime.max)

											