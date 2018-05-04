from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

class OpenLeadFilter(SimpleListFilter):
	title = 'status' # or use _('status') for translated title
	parameter_name = 'status'

	def lookups(self, request, model_admin):
		return (
		  ('Open', _('All Open')),)
		
	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(status=self.value())
		else:
			return queryset.filter(status = 'Open')
			
class SalesLeadHistoryAdmin(SimpleHistoryAdmin):
	list_display = [ "account", "owner", "probability", "next_action_description", "next_action_date"]
	#list_filter = (OpenLeadFilter,	)
	#form only show open list_display = ["sales lead", "service group", "account",  "service_line_colleagues", "last action", "next_action_date", "probability"]
	history_list_display = [ "next_action_date", "next_action_description", 'next_action_person', "user_account"]
	search_fields = ['CRM_id']
	#list_filter = ['owner', 'est_decision_date', 'status', "next_action_date"]
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
		
	def save_model(self, request, obj, form, change):
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

