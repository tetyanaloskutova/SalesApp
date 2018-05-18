from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin import SimpleListFilter, DateFieldListFilter
from django.utils.translation import ugettext_lazy as _
import datetime
import calendar

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)

class Top40Filter(SimpleListFilter):
	title = 'Top 40' 
	parameter_name = 'account__is_top40'

	def lookups(self, request, model_admin):
		return (
		  ('Yes', 'No'),)
		
	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(account=self.value())
		else:
			return queryset.filter(account = 'Open')

class FutureDateTimeFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(FutureDateTimeFilter, self).__init__(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()

        self.links += ((
            (_('Next 7 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
			(_('Next month'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(add_months(today,1)),
            }),
			(_('Next 2 months'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(add_months(today,2)),
            }),
        ))
		
class SalesLeadHistoryAdmin(SimpleHistoryAdmin):
	list_display = [ "account", "owner", "probability", "next_action_description", "next_action_date", "est_decision_date"]
	list_filter = ('account__is_top40', "next_action_date", ("est_decision_date", FutureDateTimeFilter), 'owner', 'probability')
	#form only show open list_display = ["sales lead", "service group", "account",  "service_line_colleagues", "last action", "next_action_date", "probability"]
	history_list_display = [ "next_action_date", "next_action_description", 'next_action_person', "user_account"]
	search_fields = ['CRM_id']
	#list_filter = ["next_action_date", 'owner', 'probability']
	ordering = ('-owner',)
	readonly_fields = ('user_account','CRM_id','name', 'est_revenue_USD')
	
	def account_status(self, obj):
		if obj.account.relationship_status != 'Good':
			return '<div style="width:100%%; height:100%%; background-color:orange;">%s</div>' % obj.account.relationship_status
		return obj.account.relationship_status
		
	account_status.allow_tags = True
	
	
	fieldsets = (
		('Account info', {
			'fields': ('CRM_id', ('account', 'name', 'est_revenue_USD'))
		}),
		('Next Action', {
			'fields': ( "next_action_date", "next_action_description", 'next_action_person'),
		}),
		('Service Line', {
			'fields': (('service_type', 'pm'))
		}),
		('Closure',{
			'fields': (('probability', 'est_decision_date'))
		})
	)
	def get_fields(self, request, obj=None):
		gf = super(SalesLeadHistoryAdmin, self).get_fields(request, obj)

		new_dynamic_fields = [
			('test1', forms.CharField()),
		]

		for f in new_dynamic_fields:
			#gf.append(f[0])` results in multiple instances of the new fields
			gf = gf + [f[0]]
			#updating base_fields seems to have the same effect
			self.form.declared_fields.update({f[0]})
		return gf
		
	
	def has_delete_permission(self, request, obj=None):
		return False
		
	def has_add_permission(self, request):
		return False
		
	# check this https://stackoverflow.com/questions/23361057/django-comparing-old-and-new-field-value-before-saving	
	def save_model(self, request, obj, form, change):
		print(form.cleaned_data.get('account'))
		print(form.changed_data)
		print(form.data.get('account'))
		print(change)
		print(obj.account)
		print(request.POST)
		#obj.account = form.data.get('account')
		obj.user_account = request.user
		obj.save()
		
	def get_queryset(self, request):
		qs = super(SalesLeadHistoryAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(status='Open')	

	
class AccountGroupAdmin(SimpleHistoryAdmin):	
	list_display = ('name',)
	readonly_fields = ('user_account', 'name')
	history_list_display = ( "user_account",'name')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()

class AccountAdmin(SimpleHistoryAdmin):	
	list_display = [ 'name', 'sector', 'relationship_status', 'region', 'account_manager', 'date_created']
	readonly_fields = ('user_account',)
	history_list_display = ( 'is_executive', 'is_management', 'is_user')
	ordering = ('name',)
	search_fields = ['name']
	
	fieldsets = (
		('Account info', {
			'fields': ('name', ('is_executive', 'is_management', 'is_user'), ('is_top40'))
		}),
	)
	def save_model(self, request, obj, form, change):
		obj.relationship_status = str(int(obj.is_executive) + int(obj.is_management) + int(obj.is_user))
		obj.user_account = request.user
		obj.save()

class CREmployeeAdmin(SimpleHistoryAdmin):	
	list_display = ['name', 'short_name']
	readonly_fields = ('user_account',)
	history_list_display = ( "name",'short_name')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()
		
class ServiceTypeAdmin(SimpleHistoryAdmin):	
	list_display = ('service_type','service_name')
	readonly_fields = ('user_account',)
	history_list_display = ( "user_account",'service_name')
	
	def save_model(self, request, obj, form, change):
		obj.user_account = request.user
		obj.save()

		
admin.site.register(Account, AccountAdmin)
#admin.site.register(CREmployee, CREmployeeAdmin)
#admin.site.register(ServiceType, ServiceTypeAdmin)

admin.site.register(SalesLead, SalesLeadHistoryAdmin)
#admin.site.register(AccountGroup, AccountGroupAdmin)

